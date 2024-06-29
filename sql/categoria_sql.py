SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL
    )
"""

SQL_INSERIR = """
    INSERT INTO categoria (nome, descricao)
    VALUES (?, ?)
"""

SQL_OBTER_TODAS = """
    SELECT id, nome, descricao
    FROM categoria
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM categoria
"""