class TaskNotFoundException(Exception):
    def __init__(self, message="Tarefa não encontrada"):
        self.message = message
        super().__init__(self.message)