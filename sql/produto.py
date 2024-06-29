SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        categoria INTEGER NOT NULL,
        dono INTEGER NOT NULL,
        FOREIGN KEY (categoria) REFERENCES categoria(id),
        FOREIGN KEY (dono) REFERENCES cliente(id)
    )
"""

SQL_INSERIR = """
    INSERT INTO produto (nome, descricao, categoria, dono)
    VALUES (?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT produto.id, produto.nome, produto.descricao, categoria.nome
    FROM produto
    INNER JOIN categoria ON produto.categoria=categoria.id
    WHERE dono=?
"""

SQL_OBTER_POR_ID = """
    SELECT produto.id, produto.nome, produto.descricao, categoria.nome
    FROM produto
    INNER JOIN categoria ON produto.categoria=categoria.id
    WHERE produto.id=?
"""

SQL_ALTERAR = """
    UPDATE produto
    SET nome=?, descricao=?, categoria=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM produto
    WHERE id=?
"""

SQL_PERTENCE_CLIENTE = """
    SELECT COUNT(*)
    FROM produto
    WHERE id=? AND dono=?
"""