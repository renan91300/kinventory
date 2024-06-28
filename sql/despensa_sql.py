SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS despensa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        dono INTEGER NOT NULL,
        FOREIGN KEY(dono) REFERENCES cliente(id)
    )
"""

SQL_INSERIR = """
    INSERT INTO despensa (nome, dono)
    VALUES (?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, dono
    FROM despensa
"""

SQL_ALTERAR = """
    UPDATE despensa
    SET nome=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM despensa    
    WHERE id=?
"""

SQL_PERTENCE_CLIENTE = """
    SELECT COUNT(1)
    FROM despensa
    WHERE id=? AND dono=?
"""