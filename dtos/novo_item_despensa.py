from pydantic import BaseModel


class NovoItemDespensaDTO(BaseModel):
    id_despensa: int
    id_produto: int
    quantidade: float
    data_validade: str