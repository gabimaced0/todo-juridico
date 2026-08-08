import boto3
import uuid
import os
from datetime import datetime
from dataclasses import asdict

from model.task_model import Task
from enums.task_status import TaskStatus
from exceptions.task_not_found import TaskNotFoundException


class DBService:
    """
    Gerencia a lógica de negócio das Tarefas.
    Responsável por validar regras e realizar operações no banco de dados.
    """
    def __init__(self):
        table_name = os.environ.get('TABLE_NAME')
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(table_name)

    def create_task(self, dto):
        task_id = str(uuid.uuid4())
        data_hoje = datetime.now().strftime("%d/%m/%Y")

        task = Task(
            id=task_id,
            titulo=dto.titulo,
            descricao=dto.descricao,
            status=TaskStatus.PENDENTE.value,
            criado_por=dto.criado_por,
            data_criacao=data_hoje
        )

        self.table.put_item(Item=task.to_dict())
        return task.to_dict()

    def list_tasks(self):
        response = self.table.scan()
        return response.get('Items', [])

    def get_task(self, task_id):
        response = self.table.get_item(Key={'id': task_id})
        item = response.get('Item')

        if not item:
            raise TaskNotFoundException(f"Tarefa {task_id} não encontrada.")

        return item

    def delete_task(self, task_id):
        self.table.delete_item(Key={'id': task_id})

    def update_task(self, task_id, dto):
        update_data = {k: v for k, v in asdict(dto).items() if v is not None}

        if not update_data:
            raise ValueError("Nenhum dado enviado para atualização")

        update_expression = "set "
        expression_values = {}
        expression_names = {}

        for key, value in update_data.items():
            update_expression += f"#{key} = :{key}, "
            expression_values[f":{key}"] = value
            expression_names[f"#{key}"] = key

        update_expression = update_expression.rstrip(", ")

        response = self.table.update_item(
            Key={'id': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names,
            ReturnValues="ALL_NEW"
        )
        return response.get('Attributes')