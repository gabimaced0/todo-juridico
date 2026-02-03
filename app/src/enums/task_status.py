from enum import Enum

class TaskStatus(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_