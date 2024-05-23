from flask import Flask, render_template, request, make_response, redirect, session
import basedados

def Veiculoinfo():
    render_template('veiculo/info')


def veiculo_adicionar(app):
    ligacao_bd = basedados.criar_conexao("notas.bd")
    if request.method=="GET": 
        dados=basedados.consultar_sql(ligacao_bd,"SELECT * FROM Utilizadores order by nome")
        return render_template('veiculo/adicionar.html',registos=dados)
    if request.method=="POST":
        #validar os dados
        marca = request.form.get("input_marca")
    if not marca:
        return render_template('veiculo/adicionar.html',mensagem="Preencha o campo do nome da marca do seu veículo!")
        
    categoria = request.form.get("select_categoria")
    tipo_veiculo = request.form.get("select_tipo")
    matricula = request.form.get("input_matricula")
    proibido=["#","/","\\","?"]
    for letra in proibido:
        if letra in matricula:
            return render_template('veiculo/adicionar.html',mensagem="A matricula não é válida!",registos=dados)
            
    
    id_utilizador= request.form.get("id_utilizador")
    #adicionar bd
    sql = "INSERT INTO Veiculo(marca,categoria,tipo_veiculo,matricula,id_utilizador) VALUES (?,?,?,?,?)"
    parametros = (marca,categoria,tipo_veiculo,matricula,id_utilizador)
    #fotogrfia
    fotografia=request.files["fotografia"]
    nome_fotografia=f"{matricula}.jpg"
    fotografia.save(app.config['UPLOAD_FOLDER']+"/"+nome_fotografia)    
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect ("/veiculo/listar")


def ListarMeusVeiculos():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    id_utilizador=session["id"]
    sql="""SELECT * FROM Veiculo WHERE id_utilizador=?"""
    parametros=(id_utilizador,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    print(len(dados))
    return render_template('/index.html',registos=dados)



def veiculo_listar(app):
    ligacao_bd = basedados.criar_conexao("notas.bd")
    sql = """ SELECT Veiculo.*,Utilizadores.nome as UtilizadorNome FROM Veiculo
    LEFT JOIN Utilizadores On Veiculo.id_utilizador=Utilizadores.id  
    """
    dados = basedados.consultar_sql(ligacao_bd,sql)

    return render_template('/veiculo/listar.html',registos= dados)       


def veiculo_apagar():
    matricula = request.form.get("matricula")
    #consulta a base de dados para reclher os dados do aluho selecionado
    sql = "SELECT * FROM Veiculo WHERE matricula=?"
    parametros=(matricula,)
    #executar a consulta
    ligacao_bd = basedados.criar_conexao("notas.bd")
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("veiculo/apagar.html",registo = dados[0]) 



def veiculo_apagar_comfirmado():
    matricula = request.form.get("matricula")
    sql = "DELETE FROM Veiculo WHERE matricula=?"
    parametros=(matricula,)
    ligacao_bd = basedados.criar_conexao("notas.bd")
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/veiculo/listar")

def veiculo_editar():
    matricula = request.form.get("matricula")
    #consulta à bd para recolher os dados aluno selecionado
    sql = "SELECT * FROM Veiculo WHERE matricula=?"
    parametros=(matricula,)
    #executar a consulta
    ligacao_bd = basedados.criar_conexao("notas.bd")
    dados =  basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("veiculo/editar.html",registo = dados[0])

def veiculo_editar_comfirmado(app):
    ligacao_bd = basedados.criar_conexao("notas.bd")
    matricula = request.form.get("input_matricula")

        #validar os dados
    marca = request.form.get("input_marca")
    if not marca:
        return render_template('veiculo/editar.html',mensagem="Preencha o campo da marca!")
    categoria = request.form.get("select_categqoria")
    tipo_veiculo = request.form.get("select_tipo")
    #matricula = request.form.get("matricula")

   
    #editar o aluno na bd
    sql = "UPDATE Veiculo SET marca=?, categoria=?, tipo_veiculo=? WHERE matricula=?"
    parametros = (marca,categoria,tipo_veiculo,matricula,)
    fotografia=request.files["fotografia"]
    if fotografia:
        nome_fotografia=f"{matricula}.jpg"
        fotografia.save(app.config['UPLOAD_FOLDER']+"/"+nome_fotografia)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/veiculo/listar")

def veiculo_pesquisar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    if request.method=="GET":
        return render_template('veiculo/pesquisar.html')
    if request.method=="POST":
        marca=request.form.get("input_marca")
        sql = "SELECT * FROM Veiculo WHERE marca like ?"
        marca = '%' + marca + '%'
        parametros = (marca,)
        dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
        return render_template('veiculo/pesquisar.html', registos=dados)