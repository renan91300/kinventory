from typing import Optional
from pydantic import BaseModel


class NovoProdutoDTO(BaseModel):
    id: Optional[str] = None
    nome: str
    descricao: str
    categoria: int

    