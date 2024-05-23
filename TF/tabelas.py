import basedados
import bcrypt


#CRIAR LUIGACAO A BASE DE DE DADOS
ligacao_bd=basedados.criar_conexao("notas.bd")

ativar_referencia_integridade="PRAGMA foreign_keys=ON"
basedados.executar_sql(ligacao_bd,ativar_referencia_integridade)
#TABELA PARQUE
comando_cria_tabela_parques="""
CREATE TABLE IF NOT EXISTS Parques(
    ID_parque INTEGER PRIMARY KEY,
    nome TEXT NOT NULL CHECK(length(nome)>=1),
    Local TEXT NOT NULL,
    estado TEXT CHECK(estado in ("Aberto","Fechado","Manutenção")),
    custo NUMERIC
)
""" 

basedados.executar_sql(ligacao_bd,comando_cria_tabela_parques)


#TABELA VEICULO
comando_cria_tabela_veiculos="""
CREATE TABLE IF NOT EXISTS Veiculo(
    matricula TEXT NOT NULL PRIMARY KEY,
    marca text,
    categoria text CHECK(categoria in ("Carro","Moto")),
    tipo_veiculo text,
    id_utilizador INTEGER REFERENCES Utilizadores(id)

)
"""

basedados.executar_sql(ligacao_bd,comando_cria_tabela_veiculos)

#Tabela lugar 
comando_cria_tabela_lugar="""
CREATE TABLE IF NOT EXISTS Lugar(
    ID_lugar INTEGER PRIMARY KEY,
    tipo_lugar text,
    preço text,
    ID_parque INTEGER references Parque(ID_parque) ON DELETE CASCADE
)
"""

basedados.executar_sql(ligacao_bd,comando_cria_tabela_lugar)

#tabela estacionar
comando_cria_tabela_estacionar="""
CREATE TABLE IF NOT EXISTS Estacionar(
    ID_estacionar INTEGER PRIMARY KEY,
    data_entrada numeric,
    hora_entrada numeric,
    data_saida numeric,
    hora_saida numeric,
    matricula INTEGER references Veiculo(matricula) ON DELETE CASCADE ,
    ID_lugar INTEGER references Lugar(ID_lugar) ON DELETE CASCADE

)
"""

basedados.executar_sql(ligacao_bd,comando_cria_tabela_estacionar)

#indice no parque (pesquisar)

comando_cria_indice="""
    create index nome on Parque(nome)
"""
#Utilizadores(id,nome,morada,cp,data_nasc,email,password_hash,sal,perfil,token_recuperar,data_recuperar)
tabela_utilizadores="""
CREATE TABLE IF NOT EXISTS Utilizadores(
    id INTEGER PRIMARY KEY,
    nome text not null check (length(nome)>3),
    morada text,
    cp text,
    NIF text,
    data_nasc NUMERIC,
    email text not null unique check (email like '%@%.%'),
    password_hash text not null,
    sal text not null,
    perfil text not null,
    token_recuperar text,
    data_recuperar NUMERIC
)"""
basedados.executar_sql(ligacao_bd,tabela_utilizadores)

##############################################################
# Garantir que existe um utilizador admin
#############################################################
sql="SELECT count(*) as Contar FROM Utilizadores WHERE perfil='admin'"
dados=basedados.consultar_sql(ligacao_bd,sql)

if not dados or len(dados)<1 or dados[0]["contar"]==0:
    email="admin@gmail.com"
    nome="admin"
    palavra_passe="12345"
    palavra_passe=palavra_passe.encode('utf-8')
    #gerar sal
    sal = bcrypt.gensalt()
    #hash da palavra
    palavra_hash = bcrypt.hashpw(palavra_passe,sal)
    sql = """INSERT INTO Utilizadores(nome,email,password_hash,sal,perfil) VALUES
                (?,?,?,?,'admin')"""
    parametros=(nome,email,palavra_hash,sal)
    basedados.executar_sql(ligacao_bd,sql,parametros)