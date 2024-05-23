from flask import Flask, render_template, request, make_response, redirect
import basedados


def Parquesinfo():
    return render_template('parque/info')

def ListarParquesAbertos():
    ligacao_bd=basedados.criar_conexao("notas.bd")
    estado= request.form.get("select_state")
    sql="SELECT * FROM Parques WHERE Estado='Aberto'"
    parametros=(estado)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    return dados    


def parque_adicionar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    if request.method=="GET": 
        return render_template('parque/adicionar.html')
    if request.method=="POST":
        #validar os dados
        nome = request.form.get("input_nome")
    if not nome:
        return render_template('parque/adicionar.html',mensagem="Preencha o campo do nome!")
    local = request.form.get("input_local")
    estado  = request.form.get("select_state")
    custo = request.form.get("input_custo")
    #adicionar bd
    sql = "INSERT INTO Parques(nome,local,estado,custo) VALUES (?,?,?,?)"
    parametros = (nome,local,estado,custo)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect ("/parque/listar")

def parque_listar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    sql = "SELECT * FROM Parques"
    dados = basedados.consultar_sql(ligacao_bd,sql)
    return render_template('/parque/listar.html',registos= dados)       


def parque_apagar():
    ID_parque = request.form.get("ID_parque")
    #consulta a base de dados para reclher os dados do aluho selecionado
    sql = "SELECT * FROM Parques WHERE ID_parque=?"
    parametros=(ID_parque,)
    #executar a consulta
    ligacao_bd = basedados.criar_conexao("notas.bd")
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("parque/apagar.html",registo = dados[0]) 



def parque_apagar_comfirmado():
    ID_parque = request.form.get("ID_parque")
    sql = "DELETE FROM Parques WHERE ID_parque=?"
    parametros=(ID_parque,)
    ligacao_bd = basedados.criar_conexao("notas.bd")
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/parque/listar")

def parque_editar():
    #nprocesso
    ID_parque = request.form.get("ID_parque")
    #consulta à bd para recolher os dados aluno selecionado
    sql = "SELECT * FROM Parques WHERE ID_parque=?"
    parametros=(ID_parque,)
    #executar a consulta
    ligacao_bd = basedados.criar_conexao("notas.bd")
    dados =  basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("parque/editar.html",registo = dados[0])

def parque_editar_comfirmado():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    ID_parque = request.form.get("ID_parque")
    #consulta à bd para recolher os dados aluno selecionado
    sql = "SELECT * FROM Parques WHERE ID_parque=?"
    parametros=(ID_parque,)
    #executar a consulta
    dados =  basedados.consultar_sql(ligacao_bd,sql,parametros)
    if request.method=="POST":
        #validar os dados
        nome = request.form.get("input_nome")
    if not nome:
        return render_template('parque/editar.html',mensagem="Preencha o campo do nome!")
    local = request.form.get("input_local")
    estado = request.form.get("select_state")
    custo = request.form.get("input_custo")
    ID_parque = request.form.get("ID_parque")
   
    #editar o aluno na bd
    sql = "UPDATE Parques SET nome=?, local=?, estado=?, custo=? WHERE ID_parque=?"
    parametros = (nome,local,estado,custo,ID_parque)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/parque/listar")

def parque_pesquisar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    if request.method=="GET":
        return render_template('parque/pesquisar.html')
    if request.method=="POST":
        nome=request.form.get("nome")
        sql = "SELECT * FROM Parques WHERE nome like ?"
        nome = '%' + nome + '%'
        parametros = (nome,)
        dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
        return render_template('parque/pesquisar.html', registos=dados)
    

