from datetime import datetime
from fastapi import APIRouter, Form, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse

from dtos.alterar_cliente_dto import AlterarClienteDTO
from dtos.alterar_senha_dto import AlterarSenhaDTO
from dtos.nova_despensa_dto import NovaDespensaDTO
from dtos.novo_item_despensa import NovoItemDespensaDTO
from dtos.novo_produto_dto import NovoProdutoDTO
from models.cliente_model import Cliente
from models.depensa import Despensa
from models.item_despensa import ItemDespensa
from models.produto import Produto
from repositories.categoria_repo import CategoriaRepo
from repositories.cliente_repo import ClienteRepo
from repositories.despensa_repo import DespensaRepo
from repositories.item_despensa_repo import ItemDespensaRepo
from repositories.produto import ProdutoRepo
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
    id_cliente = request.state.cliente.id

    despensas = DespensaRepo.obter_todas(id_cliente)
    return templates.TemplateResponse(
        "pages/despensa.html",
        {"request": request, "despensas": despensas},
    )


@router.get("/cadastrar_despensa")
async def get_cadastro_despensa(request: Request):
    return templates.TemplateResponse(
        "pages/cadastrar_despensa.html",
        {"request": request},
    )


@router.post("/post_cadastro_despensa", response_class=JSONResponse)
async def post_cadastro_despensa(request: Request, cadastro_dto: NovaDespensaDTO):
    despensa_data = cadastro_dto.model_dump()
    despensa_data["dono"] = request.state.cliente.id
    response = JSONResponse({"redirect": {"url": "/cliente/despensa"}})
    if DespensaRepo.inserir(Despensa(**despensa_data)):
        adicionar_mensagem_sucesso(response, "Despensa cadastrada com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível cadastrar a despensa!")
    return response


@router.get("/excluir_despensa/{id:int}")
async def get_excluir_despensa(request: Request, id: int):
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


@router.get("/itens_despensa/{id_despensa:int}")
async def get_itens_despensa(request: Request, id_despensa: int):
    id_cliente = request.state.cliente.id

    if not DespensaRepo.pertence_cliente(id_despensa, id_cliente):
        return RedirectResponse("/cliente/despensa")

    despensa = DespensaRepo.obter_por_id(id_despensa)
    itens_despensa = ItemDespensaRepo.obter_itens_por_despensa(id_despensa)

    return templates.TemplateResponse(
        "pages/itens_despensa.html",
        {
            "request": request,
            "despensa": despensa,
            "itens_despensa": itens_despensa,
        },
    )


@router.get("/cadastrar_item_despensa/{id_despensa:int}")
async def get_cadastro_item_despensa(request: Request, id_despensa: int):
    id_cliente = request.state.cliente.id
    categorias = CategoriaRepo.obter_todas()
    produtos = ProdutoRepo.obter_todos(id_cliente)

    if not DespensaRepo.pertence_cliente(id_despensa, id_cliente):
        return RedirectResponse("/cliente/despensa")

    return templates.TemplateResponse(
        "pages/cadastrar_item_despensa.html",
        {
            "request": request,
            "funcao": "cadastrar",
            "id_despensa": id_despensa,
            "categorias": categorias,
            "produtos": produtos,
            "item_despensa": None,
        },
    )

@router.get("/alterar_item_despensa/{id_despensa:int}/{id_produto:int}")
async def get_cadastro_item_despensa(request: Request, id_despensa: int, id_produto: int):
    id_cliente = request.state.cliente.id
    produtos = ProdutoRepo.obter_todos(id_cliente)

    item_despensa = ItemDespensaRepo.obter_por_id(id_despensa, id_produto)

    if not DespensaRepo.pertence_cliente(id_despensa, id_cliente):
        return RedirectResponse("/cliente/despensa")

    return templates.TemplateResponse(
        "pages/cadastrar_item_despensa.html",
        {
            "request": request,
            "funcao": "alterar",
            "produtos": produtos,
            "item_despensa": item_despensa,
            "id_despensa": id_despensa,
        },
    )


@router.post("/post_cadastro_item_despensa", response_class=JSONResponse)
async def post_cadastro_item_despensa(
    request: Request, cadastro_dto: NovoItemDespensaDTO
):
    item_despensa_data = cadastro_dto.model_dump()

    id_cliente = request.state.cliente.id
    id_despensa = item_despensa_data["id_despensa"]

    if not DespensaRepo.pertence_cliente(id_despensa, id_cliente):
        return RedirectResponse("/cliente/despensa")

    response = JSONResponse(
        {"redirect": {"url": f"/cliente/itens_despensa/{id_despensa}"}}
    )
    if ItemDespensaRepo.inserir(ItemDespensa(**item_despensa_data)):
        adicionar_mensagem_sucesso(response, "Item cadastrada com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível cadastrar o item!")
    return response

@router.post("/post_alterar_item_despensa", response_class=JSONResponse)
async def post_alterar_item_despensa(
    request: Request, cadastro_dto: NovoItemDespensaDTO
):
    item_despensa_data = cadastro_dto.model_dump()

    id_cliente = request.state.cliente.id
    id_despensa = item_despensa_data["id_despensa"]

    if not DespensaRepo.pertence_cliente(id_despensa, id_cliente):
        return RedirectResponse("/cliente/despensa")

    response = JSONResponse(
        {"redirect": {"url": f"/cliente/itens_despensa/{id_despensa}"}}
    )
    if ItemDespensaRepo.alterar(ItemDespensa(**item_despensa_data)):
        adicionar_mensagem_sucesso(response, "Item alterado com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível alterar o item!")
    return response


@router.get("/excluir_item_despensa/{id_despensa:int}/{id_produto:int}")
async def get_excluir_item_despensa(request: Request, id_despensa: int, id_produto: int):
    id_cliente = request.state.cliente.id

    if not DespensaRepo.pertence_cliente(id_despensa, id_cliente):
        return RedirectResponse("/cliente/despensa")

    response = RedirectResponse(f"/cliente/itens_despensa/{id_despensa}")

    if ItemDespensaRepo.excluir(id_despensa, id_produto):
        adicionar_mensagem_sucesso(response, "Item excluído com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível excluir o item!")
    return response


@router.get("/produtos")
async def get_produtos(request: Request):
    id_cliente = request.state.cliente.id

    produtos = ProdutoRepo.obter_todos(id_cliente)

    return templates.TemplateResponse(
        "pages/produto.html",
        {"request": request, "produtos": produtos},
    )


@router.get("/cadastrar_produto")
async def get_cadastro_produto(request: Request):
    categorias = CategoriaRepo.obter_todas()
    return templates.TemplateResponse(
        "pages/cadastrar_produto.html",
        {
            "request": request,
            "funcao": "cadastrar",
            "categorias": categorias,
            "produto": None,
        },
    )


@router.get("/alterar_produto/{id:int}")
async def get_alterar_produto(request: Request, id: int):
    categorias = CategoriaRepo.obter_todas()
    produto = ProdutoRepo.obter_por_id(id)
    if not ProdutoRepo.pertence_cliente(id, request.state.cliente.id):
        return RedirectResponse("/cliente/produtos")
    return templates.TemplateResponse(
        "pages/cadastrar_produto.html",
        {
            "request": request,
            "funcao": "alterar",
            "categorias": categorias,
            "produto": produto,
        },
    )


@router.post("/post_cadastro_produto", response_class=JSONResponse)
async def post_cadastro_produto(request: Request, cadastro_dto: NovoProdutoDTO):
    produto_data = cadastro_dto.model_dump()

    id_cliente = request.state.cliente.id
    produto_data["dono"] = id_cliente

    response = JSONResponse({"redirect": {"url": f"/cliente/produtos"}})
    if ProdutoRepo.inserir(Produto(**produto_data)):
        adicionar_mensagem_sucesso(response, "Produto cadastrada com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível cadastrar o produto!")
    return response


@router.post("/post_alterar_produto", response_class=JSONResponse)
async def post_alterar_produto(request: Request, cadastro_dto: NovoProdutoDTO):
    produto_data = cadastro_dto.model_dump()

    id_cliente = request.state.cliente.id
    produto_data["dono"] = id_cliente

    if not ProdutoRepo.pertence_cliente(produto_data["id"], id_cliente):
        return JSONResponse({"redirect": {"url": f"/cliente/produtos"}})

    response = JSONResponse({"redirect": {"url": f"/cliente/produtos"}})
    if ProdutoRepo.alterar(Produto(**produto_data)):
        adicionar_mensagem_sucesso(response, "Produto alterado com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível alterar o produto!")
    return response


@router.get("/excluir_produto/{id:int}")
async def get_excluir_produto(request: Request, id: int):
    id_cliente = request.state.cliente.id
    if not ProdutoRepo.pertence_cliente(id, id_cliente):
        return RedirectResponse("/cliente/produtos")

    response = RedirectResponse("/cliente/produtos")

    if ProdutoRepo.excluir(id):
        adicionar_mensagem_sucesso(response, "Produto excluído com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível excluir o produto!")
    return response
