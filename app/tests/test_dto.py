import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dto.task_dto import CreateTaskRequest, UpdateTaskRequest
from exceptions.invalid_task import InvalidTaskDataException


class TestTaskDTO(unittest.TestCase):

    def test_create_task_sucesso(self):
        dto = CreateTaskRequest(
            titulo="Teste Unitário",
            descricao="Validando DTO",
            criado_por="QA"
        )
        try:
            dto.validate()
        except InvalidTaskDataException:
            self.fail("DTO válido levantou erro inesperado!")

    def test_create_task_titulo_vazio(self):
        dto = CreateTaskRequest(
            titulo="",
            descricao="Descrição ok",
            criado_por="QA"
        )
        with self.assertRaises(InvalidTaskDataException) as context:
            dto.validate()

        self.assertIn("titulo", str(context.exception))

    def test_create_task_criado_por_vazio(self):
        dto = CreateTaskRequest(
            titulo="Título Ok",
            descricao="Desc",
            criado_por=""
        )
        with self.assertRaises(InvalidTaskDataException):
            dto.validate()

    def test_update_task_parcial_sucesso(self):
        dto = UpdateTaskRequest(titulo="Novo Título")
        try:
            dto.validate()
        except InvalidTaskDataException:
            self.fail("Update parcial deveria ser permitido")

    def test_update_task_status_invalido(self):
        dto = UpdateTaskRequest(status="STATUS_INEXISTENTE")

        with self.assertRaises(InvalidTaskDataException) as context:
            dto.validate()

        self.assertIn("Status 'STATUS_INEXISTENTE' inválido", str(context.exception))

    def test_update_task_data_invalida(self):
        dto = UpdateTaskRequest(data_conclusao="2026-02-03")

        with self.assertRaises(InvalidTaskDataException):
            dto.validate()

    def test_update_task_data_valida(self):
        dto = UpdateTaskRequest(data_conclusao="03/02/2026")
        try:
            dto.validate()
        except InvalidTaskDataException:
            self.fail("Data válida foi rejeitada!")
