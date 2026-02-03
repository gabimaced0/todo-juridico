import unittest
import boto3
import os
import sys
from moto import mock_aws

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from service.task_service import TaskService
from dto.task_dto import CreateTaskRequest, UpdateTaskRequest
from exceptions.task_not_found import TaskNotFoundException


@mock_aws
class TestTaskService(unittest.TestCase):

    def setUp(self):
        """
        Configura o ambiente FAKE da AWS antes de cada teste.
        """
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        os.environ['TABLE_NAME'] = 'todo-juridico-db-teste'

        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        self.table = self.dynamodb.create_table(
            TableName='todo-juridico-db-teste',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        )

        self.service = TaskService()

    def test_create_task(self):
        dto = CreateTaskRequest(titulo="Teste Moto", descricao="Real", criado_por="Dev")

        result = self.service.create_task(dto)
        task_id = result['id']

        item_no_banco = self.table.get_item(Key={'id': task_id}).get('Item')

        self.assertIsNotNone(item_no_banco)
        self.assertEqual(item_no_banco['titulo'], "Teste Moto")
        self.assertEqual(item_no_banco['status'], "Pendente")

    def test_get_task_not_found(self):
        with self.assertRaises(TaskNotFoundException):
            self.service.get_task("id-que-nao-existe")

    def test_update_task_real(self):
        self.table.put_item(Item={
            'id': '123',
            'titulo': 'Antigo',
            'status': 'Pendente',
            'descricao': 'Velha',
            'criado_por': 'Eu',
            'data_criacao': '2026-01-01'
        })

        dto = UpdateTaskRequest(titulo="Novo Título", status="Concluido")
        self.service.update_task('123', dto)

        item_atualizado = self.table.get_item(Key={'id': '123'}).get('Item')

        self.assertEqual(item_atualizado['titulo'], "Novo Título")  # Mudou?
        self.assertEqual(item_atualizado['status'], "Concluido")  # Mudou?
        self.assertEqual(item_atualizado['descricao'], "Velha")  # Manteve o resto?

    def test_delete_task(self):
        self.table.put_item(Item={'id': '999', 'titulo': 'Deletar'})

        self.service.delete_task('999')

        resp = self.table.get_item(Key={'id': '999'})
        self.assertIsNone(resp.get('Item'))
