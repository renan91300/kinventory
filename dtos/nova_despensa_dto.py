from pydantic import BaseModel


class NovaDespensaDTO(BaseModel):
    nome: str