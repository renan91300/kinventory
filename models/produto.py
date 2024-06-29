from dataclasses import dataclass
from typing import Optional


@dataclass
class Produto:
    id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[int] = None
    dono: Optional[int] = None