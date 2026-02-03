import re
from exceptions.invalid_task import InvalidTaskDataException

def validate_no_empty(value, field_name):
    """
    Valida se uma string não é nula e nem vazia/espaços em branco.
    Retorna True se estiver válida. Se for inválida, lança exceção.
    """
    if not value or not value.strip():
        raise InvalidTaskDataException(f"O campo '{field_name}' não pode ser vazio.")

def validate_date_format(date_str):
    """
    Valida se a data está no formato dd/mm/aaaa.
    """
    pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/\d{4}$"
    if not re.match(pattern, date_str):
        raise InvalidTaskDataException("A data deve estar no formato dd/mm/aaaa.")