import json
import logging
from service.db_service import DBService
from dto.task_dto import CreateTaskRequest, UpdateTaskRequest
from exceptions.invalid_task import InvalidTaskDataException
from exceptions.task_not_found import TaskNotFoundException

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class HTTPService:
    def __init__(self):
        self.service = DBService()

    def handle_request(self, event):
        try:
            http = event.get('requestContext', {}).get('http', {})
            http_method = http.get('method')
            path = http.get('path')

            logger.info(f"Requisição Recebida: {http_method} {path}")

            if http_method == 'POST' and path == '/tasks':
                body = json.loads(event.get('body', '{}'))
                dto = CreateTaskRequest(
                    titulo=body.get('titulo'),
                    descricao=body.get('descricao', ''),
                    criado_por=body.get('criado_por')
                )
                dto.validate()
                result = self.service.create_task(dto)
                return self.build_response(201, result)

            elif http_method == 'GET' and path == '/tasks':
                result = self.service.list_tasks()
                return self.build_response(200, result)

            elif http_method == 'GET' and path.startswith('/tasks/'):
                task_id = path.split('/')[-1]
                result = self.service.get_task(task_id)
                return self.build_response(200, result)

            elif http_method == 'PUT' and path.startswith('/tasks/'):
                task_id = path.split('/')[-1]
                body = json.loads(event.get('body', '{}'))

                dto = UpdateTaskRequest(
                    titulo=body.get('titulo'),
                    descricao=body.get('descricao'),
                    status=body.get('status'),
                    data_conclusao=body.get('data_conclusao')
                )
                dto.validate()

                result = self.service.update_task(task_id, dto)
                return self.build_response(200, result)

            elif http_method == 'DELETE' and path.startswith('/tasks/'):
                task_id = path.split('/')[-1]
                self.service.delete_task(task_id)
                return self.build_response(204, None)

            else:
                return self.build_response(404, {'error': 'Rota não encontrada'})

        except TaskNotFoundException as e:
            return self.build_response(404, {'error': e.message})

        except (ValueError, InvalidTaskDataException) as e:
            return self.build_response(400, {'error': str(e)})

        except Exception as e:
            logger.error(f"Erro Crítico: {e}", exc_info=True)
            return self.build_response(500, {'error': 'Erro Interno do Servidor'})

    def build_response(self, status_code, body):
        body_log = body if body is not None else "No Content"

        logger.info(f"Status: {status_code} | Body: {json.dumps(body_log, default=str)}")

        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps(body) if body is not None else None
        }