from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Task:
    """
    Define a estrutura dos campos e converte o objeto para formato de
    dicionário compatível com o banco de dados.
    """
    id: str
    titulo: str
    descricao: str
    status: str
    criado_por: str
    data_criacao: str
    data_conclusao: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}