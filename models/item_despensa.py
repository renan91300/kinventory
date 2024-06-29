from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemDespensa:
    id_despensa: Optional[int] = None
    id_produto: Optional[int] = None
    quantidade: Optional[float] = None
    data_validade: Optional[str] = None