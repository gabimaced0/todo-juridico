from dataclasses import dataclass
from typing import Optional
from enums.task_status import TaskStatus
from exceptions.invalid_task import InvalidTaskDataException
from utils.validators import validate_no_empty, validate_date_format

@dataclass
class CreateTaskRequest:
    """
    Objeto de Transferência de Dados (DTO) responsável pela entrada de dados na criação
    de tarefas.
    Garante a integridade e validação dos campos obrigatórios antes do processamento.
    """
    titulo: str
    descricao: str
    criado_por: str

    def validate(self):
        validate_no_empty(self.titulo, "titulo")
        validate_no_empty(self.criado_por, "criado_por")


@dataclass
class UpdateTaskRequest:
    """
    Objeto de Transferência de Dados (DTO) para atualização de tarefas.
    Suporta atualização parcial (campos opcionais) e aplica validações específicas de
    negócio nos dados fornecidos.
    """
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None
    data_conclusao: Optional[str] = None

    def validate(self):

        if self.titulo is not None:
            validate_no_empty(self.titulo, "titulo")

        if self.status is not None:
            if not TaskStatus.has_value(self.status):
                valid_options = [e.value for e in TaskStatus]
                raise InvalidTaskDataException(
                    f"Status '{self.status}' inválido. Opções: {valid_options}"
                )

        if self.data_conclusao is not None:
            validate_date_format(self.data_conclusao)