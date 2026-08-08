from service.http_service import HTTPService

http_service = HTTPService()

def lambda_handler(event, context):
    return http_service.handle_request(event)