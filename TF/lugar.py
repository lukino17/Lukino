from flask import Flask, render_template, request, make_response, redirect
import basedados


def Lugar_info():
    return render_template('lugar/info')


def lugar_adicionar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    #verificar se o metodo e GET
    if request.method=="GET": 
        parques = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Parques ORDER BY nome")
        return render_template('lugar/adicionar.html', parques = parques)
    if request.method=="POST":
        ID_parque = request.form.get("ID_parque")
        tipo_lugar = request.form.get("input_typelugar")
        preço = request.form.get("input_preco")    
    #inserir a bd
    sql = "INSERT INTO Lugar(ID_parque,tipo_lugar,preço) VALUES(?,?,?) " 
    parametros = (ID_parque,tipo_lugar,preço)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/lugar/listar")


def lugar_listar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    sql = """ SELECT Lugar.*,parques.nome as ParqueNome FROM Lugar
    LEFT JOIN Parques On Lugar.ID_parque=Parques.ID_parque  
    """
    dados = basedados.consultar_sql(ligacao_bd,sql)
    sql = """SELECT Parques.nome as ParqueNome,avg(preço) as media 
            FROM Lugar LEFT JOIN Parques 
            ON Lugar.ID_parque=Parques.ID_parque
            GROUP BY Lugar.ID_parque,Parques.nome"""
    medias = basedados.consultar_sql(ligacao_bd,sql)
    return render_template('/lugar/listar.html',registos= dados,medias= medias) 


def lugar_apagar():
    ID_lugar = request.form.get("ID_lugar")
    #consulta a base de dados para reclher os dados do aluho selecionado
    sql = """SELECT Lugar.*,parques.nome as ParqueNome FROM Lugar
    LEFT JOIN Parques On Lugar.ID_parque=Parques.ID_parque 
    WHERE Lugar.ID_lugar=?
    """
    parametros=(ID_lugar,)
    #executar a consulta
    ligacao_bd = basedados.criar_conexao("notas.bd")
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("lugar/apagar.html",registo = dados[0]) 



def lugar_apagar_comfirmado():
    ID_lugar = request.form.get("ID_lugar")
    sql = "DELETE FROM Lugar WHERE ID_lugar=?"
    parametros=(ID_lugar,)  
    ligacao_bd = basedados.criar_conexao("notas.bd")
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/lugar/listar")

def lugar_editar():
    #nprocesso
    ligacao_bd = basedados.criar_conexao("notas.bd")
    parques = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Parques ORDER BY nome")
    ID_lugar = request.form.get("ID_lugar")
    sql = "SELECT * FROM Lugar WHERE ID_lugar=?"
    parametros=(ID_lugar,)
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    #verificar se o metodo e GET
    return render_template('lugar/editar.html', parques = parques, registo=dados[0])

def lugar_editar_comfirmado():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    ID_lugar = request.form.get("ID_lugar")
    sql = "SELECT * FROM Lugar WHERE ID_lugar=?"
    parametros = (ID_lugar,)
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    #validar os dados
    parques = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Parques ORDER BY nome")
    ID_parque = request.form.get("ID_parque")
    tipo_lugar = request.form.get("input_typelugar")
    preço = request.form.get("input_preco")
    
    #TODO guardar fotografia
    #adicionar bd
    sql = "UPDATE Lugar SET ID_parque=?, tipo_lugar=?, preço=? WHERE ID_lugar=?"
    parametros = (ID_parque,tipo_lugar,preço,ID_lugar)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/lugar/listar")