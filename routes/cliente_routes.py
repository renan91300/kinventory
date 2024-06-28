from datetime import datetime
from fastapi import APIRouter, Form, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse

from dtos.alterar_cliente_dto import AlterarClienteDTO
from dtos.alterar_senha_dto import AlterarSenhaDTO
from dtos.nova_despensa_dto import NovaDespensaDTO
from models.cliente_model import Cliente
from models.depensa import Despensa
from repositories.cliente_repo import ClienteRepo
from repositories.despensa_repo import DespensaRepo
from util.auth import conferir_senha, obter_hash_senha
from util.cookies import (
    adicionar_mensagem_alerta,
    adicionar_mensagem_erro,
    adicionar_mensagem_sucesso,
    excluir_cookie_auth,
)
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/cliente")
templates = obter_jinja_templates("templates/cliente")

@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse(
        "pages/cadastro.html",
        {
            "request": request,
        },
    )


@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(request: Request, alterar_dto: AlterarClienteDTO):
    id = request.state.cliente.id
    cliente_data = alterar_dto.model_dump()
    response = JSONResponse({"redirect": {"url": "/cliente/cadastro"}})
    if ClienteRepo.alterar(Cliente(id, **cliente_data)):
        adicionar_mensagem_sucesso(response, "Cadastro alterado com sucesso!")
    else:
        adicionar_mensagem_erro(
            response, "Não foi possível alterar os dados cadastrais!"
        )
    return response


@router.get("/senha")
async def get_senha(request: Request):
    return templates.TemplateResponse(
        "pages/senha.html",
        {"request": request},
    )


@router.post("/post_senha", response_class=JSONResponse)
async def post_senha(request: Request, alterar_dto: AlterarSenhaDTO):
    email = request.state.cliente.email
    cliente_bd = ClienteRepo.obter_por_email(email)
    nova_senha_hash = obter_hash_senha(alterar_dto.nova_senha)
    response = JSONResponse({"redirect": {"url": "/cliente/senha"}})
    if not conferir_senha(alterar_dto.senha, cliente_bd.senha):
        adicionar_mensagem_erro(response, "Senha atual incorreta!")
        return response
    if ClienteRepo.alterar_senha(cliente_bd.id, nova_senha_hash):
        adicionar_mensagem_sucesso(response, "Senha alterada com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível alterar sua senha!")
    return response



@router.get("/sair", response_class=RedirectResponse)
async def get_sair(request: Request):
    if request.state.cliente:
        ClienteRepo.alterar_token(request.state.cliente.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    excluir_cookie_auth(response)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso!")
    return response


@router.get("/despensa")
async def get_despensa(request: Request):
    despensas = DespensaRepo.obter_todas()
    return templates.TemplateResponse(
        "pages/despensa.html",
        {"request": request, "despensas": despensas},
    )

@router.get("/cadastrardespensa")
async def get_cadastro_despensa(request: Request):
    return templates.TemplateResponse(
        "pages/cadastrar_despensa.html",
        {"request": request},
    )

@router.post("/post_cadastro_despensa", response_class=JSONResponse)
async def post_cadastro(request: Request, cadastro_dto: NovaDespensaDTO):
    despensa_data = cadastro_dto.model_dump()
    despensa_data["dono"] = request.state.cliente.id
    response = JSONResponse({"redirect": {"url": "/cliente/despensa"}})
    if DespensaRepo.inserir(Despensa(**despensa_data)):
        adicionar_mensagem_sucesso(response, "Despensa cadastrada com sucesso!")
    else:
        adicionar_mensagem_erro(
            response, "Não foi possível cadastrar a despensa!"
        )
    return response

@router.get("/excluirdespensa/{id:int}")
async def get_excluir_despensa(
    request: Request, id: int
): 
    id_cliente = request.state.cliente.id

    response = RedirectResponse("/cliente/despensa")

    if not DespensaRepo.pertence_cliente(id, id_cliente):
        adicionar_mensagem_erro(response, "Despensa não encontrada!")
        return response

    if DespensaRepo.excluir(id):
        adicionar_mensagem_sucesso(response, "Despensa excluída com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível excluir a despensa!")
    return response

