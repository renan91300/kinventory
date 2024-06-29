SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS itens_despensa (
        id_despensa INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade REAL NOT NULL,
        data_validade TEXT NOT NULL,
        PRIMARY KEY (id_despensa, id_produto),
        FOREIGN KEY (id_despensa) REFERENCES despensas(id),
        FOREIGN KEY (id_produto) REFERENCES produtos(id)
    )
"""

SQL_INSERIR = """
    INSERT INTO itens_despensa (id_despensa, id_produto, quantidade, data_validade)
    VALUES (?, ?, ?, ?)
"""

SQL_OBTER_ITENS_POR_DESPENSA = """
    SELECT produto.id AS id_produto, produto.nome, itens_despensa.quantidade, itens_despensa.data_validade
    FROM itens_despensa
    INNER JOIN produto ON itens_despensa.id_produto=produto.id
    WHERE itens_despensa.id_despensa=?
"""

SQL_OBTER_POR_ID = """
    SELECT id_despensa, id_produto, quantidade, data_validade
    FROM itens_despensa
    WHERE id_despensa=? AND id_produto=?
"""

SQL_ALTERAR = """
    UPDATE itens_despensa
    SET quantidade=?, data_validade=?, id_produto=?
    WHERE id_despensa=? AND id_produto=?
"""

SQL_EXCLUIR = """
    DELETE FROM itens_despensa
    WHERE id_despensa=? AND id_produto=?
"""
