import json
import sqlite3
from typing import List, Optional
from models.depensa import Despensa
from sql.despensa_sql import *
from util.database import obter_conexao


class DespensaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, despensa: Despensa) -> Optional[Despensa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        despensa.nome,
                        despensa.dono
                    ),
                )
                if cursor.rowcount > 0:
                    despensa.id = cursor.lastrowid
                    return despensa
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todas(cls) -> List[Despensa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                despensas = [Despensa(*t) for t in tuplas]
                return despensas
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, despensa: Despensa) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        despensa.nome,
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
    def pertence_cliente(cls, id_despensa: int, id_cliente: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_PERTENCE_CLIENTE, (id_despensa, id_cliente))
                return cursor.fetchone() is not None
        except sqlite3.Error as ex:
            print(ex)
            return False