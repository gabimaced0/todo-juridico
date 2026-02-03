class InvalidTaskDataException(Exception):
    def __init__(self, message="Dados da tarefa inválidos"):
        self.message = message
        super().__init__(self.message)