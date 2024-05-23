from flask import Flask, render_template, request, make_response, redirect
import basedados


def Estacionarinfo():
    render_template('estacionar/info')

def estacionar_adicionar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    #verificar se o metodo e GET
    lugares = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Lugar ORDER BY ID_lugar")
    veiculos = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Veiculo")
    if request.method=="GET": 

        return render_template('estacionar/adicionar.html', veiculos = veiculos, lugares = lugares)
    if request.method=="POST":
        ID_lugar = request.form.get("ID_lugar")
        matricula = request.form.get("input_matricula")
        data_entrada = request.form.get("input_data_ent")
        hora_entrada = request.form.get("input_hora_ent")
        data_saida  = request.form.get("input_data_sai")
        hora_saida = request.form.get("input_hora_sai")
#se fosse no mesmo dia 
        if  data_entrada > data_saida:
            return render_template('estacionar/adicionar.html', veiculos=veiculos, lugares=lugares, mensagem="A data de entrada não podem ser maior que a data de saida!")
    
        if  data_entrada==data_saida and hora_entrada > hora_saida:
            return render_template('estacionar/adicionar.html', veiculos=veiculos, lugares=lugares, mensagem="A hora de entrada nao pode ser maior que a hora de saida se não for no mesmo dia") #mudar a mensagem!!
        
        if not ID_lugar:
            return render_template('estacionar/adicionar.html', veiculos=veiculos, lugares=lugares, mensagem="O campo do ID do lugar é obrigatorio!")

    #inserir a bd
    sql = "INSERT INTO Estacionar(ID_lugar,matricula,data_entrada,hora_entrada,data_saida,hora_saida) VALUES(?,?,?,?,?,?) " 
    parametros = (ID_lugar,matricula,data_entrada,hora_entrada,data_saida,hora_saida)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/estacionar/listar")
    
def estacionar_listar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    sql = """ SELECT Estacionar.*,Lugar.ID_lugar,Veiculo.matricula FROM Estacionar
    LEFT JOIN Lugar On Estacionar.ID_lugar=Lugar.ID_lugar
    LEFT JOIN Veiculo On Estacionar.matricula=Veiculo.matricula
    """
    
    dados = basedados.consultar_sql(ligacao_bd,sql)
    return render_template('/estacionar/listar.html',registos= dados) 

def estacionar_apagar():
    ID_estacionar = request.form.get("ID_estacionar")
    #consulta a base de dados para reclher os dados do aluho selecionado
    sql = """SELECT Estacionar.*,Lugar.ID_lugar,Veiculo.matricula FROM Estacionar
    LEFT JOIN Lugar On Estacionar.ID_lugar=Lugar.ID_lugar
    LEFT JOIN Veiculo On Estacionar.matricula=Veiculo.matricula
    WHERE Estacionar.ID_estacionar=?
    """
    parametros=(ID_estacionar,)
    #executar a consulta
    ligacao_bd = basedados.criar_conexao("notas.bd")
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("estacionar/apagar.html",registo = dados[0]) 



def estacionar_apagar_comfirmado():
    ID_estacionar = request.form.get("ID_estacionar")
    sql = "DELETE FROM Estacionar WHERE ID_estacionar=?"
    parametros=(ID_estacionar,)
    ligacao_bd = basedados.criar_conexao("notas.bd")
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/estacionar/listar")

def estacionar_editar():
    #nprocesso
    ligacao_bd = basedados.criar_conexao("notas.bd")
    veiculos = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Veiculo ORDER BY marca")
    lugares = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Lugar ORDER BY tipo_lugar")
    ID_estacionar = request.form.get("ID_estacionar")
    sql = "SELECT * FROM Estacionar WHERE ID_estacionar=?"
    parametros=(ID_estacionar,)
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    #verificar se o metodo e GET
    return render_template('estacionar/editar.html', veiculos = veiculos, lugares = lugares, registo=dados[0])

def estacionar_editar_comfirmado():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    ID_estacionar = request.form.get("ID_estacionar")
    sql = "SELECT * FROM Estacionar WHERE ID_estacionar=?"
    parametros = (ID_estacionar,)
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    #validar os dados
    lugares = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Lugar ORDER BY tipo_lugar")
    veiculos = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Veiculo ORDER BY matricula")
    matricula = request.form.get("matricula")
    ID_lugar = request.form.get("ID_lugar")
    data_entrada = request.form.get("input_data_ent")
    hora_entrada = request.form.get("input_hora_ent")
    data_saida = request.form.get("input_data_sai")
    hora_saida = request.form.get("input_hora_sai")

    if  data_entrada > data_saida:
            return render_template('estacionar/adicionar.html', veiculos=veiculos, lugares=lugares, mensagem="A data de entrada não podem ser maior que a data de saida!")
    
    if data_entrada==data_saida and hora_entrada > hora_saida:
            return render_template('estacionar/adicionar.html', veiculos=veiculos, lugares=lugares, mensagem="A hora de entrada não podem ser maior que a hora de saida!")
    
    if not ID_lugar:
            return render_template('estacionar/adicionar.html', veiculos=veiculos, lugares=lugares, mensagem="O campo do ID do lugar é obrigatorio!")
    
    #TODO guardar fotografia
    #adicionar bd
    sql = "UPDATE Estacionar SET matricula=?, ID_lugar=?, data_entrada=?, hora_entrada=?, data_saida=?, hora_saida=? WHERE ID_estacionar=?"
    parametros = (matricula,ID_lugar,data_entrada,hora_entrada,data_saida,hora_saida,ID_estacionar)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/estacionar/listar")