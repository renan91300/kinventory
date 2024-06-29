import json
import sqlite3
from typing import List, Optional
from models.produto import Produto
from sql.produto import *
from util.database import obter_conexao


class ProdutoRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, produto: Produto) -> Optional[Produto]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        produto.nome,
                        produto.descricao,
                        produto.categoria,
                        produto.dono,
                    ),
                )
                if cursor.rowcount > 0:
                    produto.id = cursor.lastrowid
                    return produto
        except sqlite3.Error as ex:
            print(ex)
            return None



    @classmethod
    def obter_todos(cls, id_cliente: int) -> List[Produto]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS, (id_cliente,)).fetchall()
                produtos = [Produto(*t) for t in tuplas]
                return produtos
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Produto]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id,)).fetchone()
                return Produto(*tupla)
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, produto: Produto) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        produto.nome,
                        produto.descricao,
                        produto.categoria,
                        produto.id,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
    
    @classmethod
    def pertence_cliente(cls, id: int, id_cliente: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_PERTENCE_CLIENTE, (id, id_cliente))
                return cursor.fetchone()[0] > 0
        except sqlite3.Error as ex:
            print(ex)
            return False