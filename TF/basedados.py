import sqlite3

def criar_conexao(nome_arquivo):
    """Cria uma conexão com a base de dados especificada pelo nome do arquivo."""
    conexao = None
    try:
        conexao = sqlite3.connect(nome_arquivo)
        conexao.row_factory = sqlite3.Row
        print("Conexão estabelecida com a base de dados")
    except sqlite3.Error as e:
        print(f"Erro ao conectar com a base de dados: {e}")
    return conexao

def executar_sql(conexao, comando_sql, parametros=None):
    """Executa um comando SQL passado como parâmetro, com parâmetros opcionais."""
    try:
        cursor = conexao.cursor()
        if parametros:
            cursor.execute(comando_sql, parametros)
        else:
            cursor.execute(comando_sql)
        conexao.commit()
        print("Comando SQL executado com sucesso")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao executar o comando SQL: {e}")

def consultar_sql(conexao,sql,parametros=None):
    """Executa uma consulta SQL e devolve os resultados com os nomes dos campos"""
    try:
        cursor = conexao.cursor()
        if parametros==None:
            cursor.execute(sql)
        else:
            cursor.execute(sql,parametros)
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return None