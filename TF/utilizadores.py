from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import basedados
import requests
import bcrypt
import random
import re

RECAPTCHA_SITE_KEY="6LdigYIpAAAAAJGfpZWySe7yuKo61E9GG3pzCEcP"
RECAPTCHA_SECRET_KEY="6LdigYIpAAAAAFp6nHlosWycTpglAC-bbxUe_QyB"

def Utilizadores_info():
    render_template('/Utilizadores/info')


def RegistoUtilizador():
    if request.method=="GET":
        return render_template("utilizadores/registo.html",site_key=RECAPTCHA_SITE_KEY)
    if request.method=="POST":
        ligacao_bd=basedados.criar_conexao("notas.bd")
        #verificar o reCAPTCHA
        recaptcha_response = request.form['g-recaptcha-response']
        payload={'response':recaptcha_response,'secret':RECAPTCHA_SECRET_KEY}
        response=requests.post('https://www.google.com/recaptcha/api/siteverify',data=payload)
        response_data=response.json()
        print(response_data)
        if response_data["success"]==True:
            nome=request.form.get("nome")
            email=request.form.get("email")
            palavra_passe=request.form.get("password")
            #verificar se o email está repetido
            if not nome or not email:
                return render_template("utilizadores/registo.html",site_key=RECAPTCHA_SITE_KEY,mensagem="Tem de indicar um nome e um email.")
            # Validações de senha
            if len(palavra_passe) < 2:
                return render_template("utilizadores/registo.html", site_key=RECAPTCHA_SITE_KEY, mensagem="A senha deve ter pelo menos 2 caracteres.")
            if not re.search("[0-9]", palavra_passe):
                return render_template("utilizadores/registo.html", site_key=RECAPTCHA_SITE_KEY, mensagem="A senha deve conter pelo menos um número.")
            sql="SELECT count(*) as Contar FROM Utilizadores WHERE email=?"
            parametros=(email,)
            dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
            if dados and dados[0]["Contar"]>0:
                return render_template("utilizadores/registo.html",site_key=RECAPTCHA_SITE_KEY,mensagem="Esse email já existe na nossa base de dados.")
            #inserir na bd
            palavra_passe=palavra_passe.encode('utf-8')
            #gerar sal
            sal = bcrypt.gensalt()
            #hash da palavra
            palavra_hash = bcrypt.hashpw(palavra_passe,sal)
            sql = """INSERT INTO Utilizadores(nome,email,password_hash,sal,perfil) VALUES
                        (?,?,?,?,'user')"""
            parametros=(nome,email,palavra_hash,sal)
            basedados.executar_sql(ligacao_bd,sql,parametros)
            #TODO: Redirecionar para ?????
            return render_template("utilizadores/registo_sucesso.html")
        else:
            return render_template("utilizadores/registo.html",site_key=RECAPTCHA_SITE_KEY,mensagem="Tem de provar que não é um robot.")

def Login():
    if request.method=="POST":
        email=request.form.get("email")
        palavra_passe=request.form.get("password")
        ligacao_bd=basedados.criar_conexao("notas.bd")
        sql="SELECT password_hash,id,perfil,nome FROM Utilizadores WHERE email=?"
        parametros=(email,)
        dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
        if dados:
            if dados[0]['perfil']=='bloqueado':
                return render_template("index.html",mensagem="A sua conta de utilizador encontra-se bloqueada. Contacte o administrador para mais informações.")
            password_hash=dados[0]["password_hash"]
            if bcrypt.checkpw(palavra_passe.encode('utf-8'),password_hash):
                #iniciar sessão
                session["email"]=email
                session["id"]=dados[0]["id"]
                session["perfil"]=dados[0]["perfil"]
                session["nome"]=dados[0]["nome"]
                return redirect("/")
        print("Login falhou")
        return render_template("index.html",mensagem="Login falhou. Tente novamente.")

def Logout():
    session.clear()
    return redirect("/")

def Logado():
    if "email" in session:
        return True
    return False

def Utilizador_E_Admin():
    if Logado() and session["perfil"]=='admin':
        return True
    return False

#função para gerar um token que será guardado na base de dados e posteriormente 
#enviado ao utilizador por email
def CriarToken(email_destino):
    token=random.randint(100000,999999) #TODO: substituir or UUID
    ligacao_bd=basedados.criar_conexao("notas.bd")
    sql="UPDATE Utilizadores SET token_recuperar=? WHERE email=?"
    parametros=(token,email_destino)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return token

#alterar a password do utilizador com o token indicado
def Nova_Password(token,password):
    #verificar o reCAPTCHA
    ligacao_bd=basedados.criar_conexao("notas.bd")
    #verificar o reCAPTCHA
    recaptcha_response = request.form['g-recaptcha-response']
    payload={'response':recaptcha_response,'secret':RECAPTCHA_SECRET_KEY}
    response=requests.post('https://www.google.com/recaptcha/api/siteverify',data=payload)
    response_data=response.json()
    print(response_data)
    if response_data["success"]==True:
        palavra_passe=password.encode('utf-8')
            #gerar sal
        sal = bcrypt.gensalt()
            #hash da palavra
        palavra_hash = bcrypt.hashpw(palavra_passe,sal)
        sql="UPDATE Utilizadores SET password_hash=?, token_recuperar=null WHERE token_recuperar=?"
        parametros=(palavra_hash,token)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        return redirect("/")
    else:
        return render_template("utilizadores/recuperar_password.html",token=token,site_key=RECAPTCHA_SITE_KEY,mensagem="Tem de provar que não é um robot.")

#Função para listar todos os utilizadores registados na página listar.html da pasta utilizadores
#Só para admin
def Listar():
    ligacao_bd=basedados.criar_conexao("notas.bd")
    #se é admin lista todos
    if Utilizador_E_Admin():
        dados=basedados.consultar_sql(ligacao_bd,"SELECT * FROM Utilizadores")
    #se não é admin lista os utilizadores do utilizador logado
    else:
        sql="SELECT * FROM Utilizadores WHERE id=?"
        parametros=(session["id"],)
        dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("utilizadores/listar.html",registos=dados)

#Só para admin
def Adicionar():
    ligacao_bd=basedados.criar_conexao("notas.bd")
    if request.method=="GET":
        return render_template("utilizadores/adicionar.html")
    if request.method=="POST":
        nome=request.form.get("nome")
        email=request.form.get("email")
        morada=request.form.get("morada")
        cp=request.form.get("cp")
        password=request.form.get("password")
        palavra_passe=password.encode('utf-8')
        perfil=request.form.get("perfil")
        #gerar sal
        sal = bcrypt.gensalt()
        #hash da palavra
        palavra_hash = bcrypt.hashpw(palavra_passe,sal)
        sql="INSERT INTO Utilizadores(nome,email,morada,cp,password_hash,perfil,sal) VALUES(?,?,?,?,?,?,?)"
        parametros=(nome,email,morada,cp,palavra_hash,perfil,sal)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        return redirect("/Utilizadores/listar")

#Só para admin
def Apagar():
    id=request.form.get("id")
    ligacao_bd=basedados.criar_conexao("notas.bd")
    sql="SELECT email,nome,id FROM Utilizadores WHERE id=?"
    parametros=(id,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("utilizadores/apagar.html",utilizador=dados[0])

#Só para admin
def ApagarConfirmado():
    id=request.form.get("id")
    ligacao_bd=basedados.criar_conexao("notas.bd")
    sql="DELETE FROM Utilizadores WHERE id=?"
    parametros=(id,)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/Utilizadores/listar")

#Só para admin
def Editar():
    id=request.form.get("id")
    ligacao_bd=basedados.criar_conexao("notas.bd")
    sql="SELECT email,nome,id,morada,cp,data_nasc FROM Utilizadores WHERE id=?"
    parametros=(id,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("utilizadores/editar.html",utilizador=dados[0])

def EditarPerfil():
    id=session["id"]
    print(id)
    ligacao_bd=basedados.criar_conexao("notas.bd")
    sql="SELECT email,nome,id,morada,cp,data_nasc FROM Utilizadores WHERE id=?"
    parametros=(id,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("utilizadores/editar_perfil.html",utilizador=dados[0])

#Só para admin
def EditarConfirmado():
    id=request.form.get("id")
    nome=request.form.get("nome")
    email=request.form.get("email")
    morada=request.form.get("morada")
    cp=request.form.get("cp")
    data_nasc=request.form.get("data_nasc")
    ligacao_bd=basedados.criar_conexao("notas.bd")
    sql="UPDATE Utilizadores SET nome=?,email=?,morada=?,cp=?,data_nasc=? WHERE id=?"
    parametros=(nome,email,morada,cp,data_nasc,id)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/Utilizadores/listar")

def Bloquear():
    ligacao_bd=basedados.criar_conexao("notas.bd")
    id=request.form.get("id")
    perfil="bloqueado"
    sql="UPDATE Utilizadores SET perfil=? WHERE id=?"
    parametros=(perfil,id)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/Utilizadores/listar")

def MudarPerfil():
    ligacao_bd=basedados.criar_conexao("notas.bd")
    id=request.form.get("id")
    perfil="admin"
    sql="SELECT perfil FROM Utilizadores WHERE id=?"
    parametros=(id,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    if dados[0]['perfil']=='admin':
        perfil="user"
    sql="UPDATE Utilizadores SET perfil=? WHERE id=?"
    parametros=(perfil,id)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/Utilizadores/listar")