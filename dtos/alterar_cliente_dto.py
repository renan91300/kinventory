from pydantic import BaseModel, field_validator
from datetime import date, datetime, timedelta

from util.validators import *


class AlterarClienteDTO(BaseModel):    
    nome: str
    cpf: str
    data_nascimento: str
    telefone: str
    email: str

    @field_validator("nome")
    def validar_nome(cls, v):
        msg = is_person_fullname(v, "Nome")
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("cpf")
    def validar_cpf(cls, v):
        msg = is_cpf(v, "CPF")
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("data_nascimento")
    def validar_data_nascimento(cls, v):
        msg = is_not_empty(v, "Data de Nascimento")
        if not msg:
            msg = is_date_valid(v, "Data de Nascimento")
        if not msg:
            data_minima = date.today() - timedelta(days=125 * 365)
            data_v = datetime.strptime(v, "%Y-%m-%d").date()
            msg = is_date_between(
                data_v, "Data de Nascimento", data_minima, date.today()
            )
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("telefone")
    def validar_telefone(cls, v):
        msg = is_phone_number(v, "Telefone")
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("email")
    def validar_email(cls, v):
        msg = is_email(v, "E-mail")
        if msg:
            raise ValueError(msg)
        return v