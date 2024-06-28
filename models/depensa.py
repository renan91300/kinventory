from dataclasses import dataclass
from typing import Optional


@dataclass
class Despensa:
    id: Optional[int] = None
    nome: Optional[str] = None
    dono: Optional[int] = None