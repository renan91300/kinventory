import json
import sqlite3
from typing import Dict, List, Optional
from models.item_despensa import ItemDespensa
from sql.item_despensa import *
from util.database import obter_conexao


class ItemDespensaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, item_despensa: ItemDespensa) -> Optional[ItemDespensa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        item_despensa.id_despensa,
                        item_despensa.id_produto,
                        item_despensa.quantidade,
                        item_despensa.data_validade,
                    ),
                )
                if cursor.rowcount > 0:
                    item_despensa.id = cursor.lastrowid
                    return item_despensa
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_itens_por_despensa(cls, id_despensa: int) -> List[Dict]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_OBTER_ITENS_POR_DESPENSA, (id_despensa,))
                cursor.row_factory = sqlite3.Row
                item_despensas = cursor.fetchall()
                return item_despensas
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_por_id(cls, id_despensa: int, id_produto) -> Optional[ItemDespensa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id_despensa, id_produto)).fetchone()
                return ItemDespensa(*tupla)
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, item_despensa: ItemDespensa) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        item_despensa.quantidade,
                        item_despensa.data_validade,
                        item_despensa.id_produto,
                        item_despensa.id_despensa,
                        item_despensa.id_produto,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def excluir(cls, id_despensa: int, id_produto: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id_despensa, id_produto,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False