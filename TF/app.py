from flask import Flask, render_template, request, redirect, session,make_response, jsonify
from flask_session import Session
from flask_mail import Mail, Message
import os
import basedados
import parque
import tabelas
import veiculo
import lugar
import estacionar
import utilizadores
import veiculo
from flask_session import Session
import os
from flask_mail import Mail, Message
import config

#TODO ALTERAR O ESTADO (cOnsiderando ainda)//arrumar o bglh de admin e ver mais coisa mas ja vai tocar tbm kkk 

app = Flask(__name__)

config.config_upload(app)

#configuração dos cookies de sessão
config.config_session(app)

#configuração do email
config.config_mail(app)

mail=Mail(app)

#rota index
#ROTAS PUBLICAS
@app.route('/')
def index():
    if utilizadores.Logado():
        if utilizadores.Utilizador_E_Admin():
            dados=parque.ListarParquesAbertos()
        else:
            return veiculo.ListarMeusVeiculos()
    else:
        dados=[]
    return render_template("index.html",registos=dados)
    
@app.route('/aceitar_cookies',methods=['POST'])
def aceitar_cookies():

    resposta = make_response(redirect("/"))
    #cookie com prazo de validade de 30 dias
    resposta.set_cookie('aviso','aceitou',max_age=30*24*60*60)
    return resposta

@app.route('/404/autor', methods=["GET"])
def autor():
    return render_template('404/autor.html')

@app.route('/Utilizadores/registo',methods=["POST","GET"])
def Registo():
        return utilizadores.RegistoUtilizador()

@app.route('/Login',methods=["POST"])
def Login():
        return utilizadores.Login()

@app.route('/recuperar_password',methods=['POST','GET'])
def RecuperarPassword():
    token=request.args.get("token",None)
    #se o utilizador não tem token (1º passo)
    if token is None and request.method=="GET":
        #enviar email para utilizador com o token
        email_destino=request.args.get("email")
        token = str(utilizadores.CriarToken(email_destino))
        assunto="Recuperação de palavra passe"
        texto="Clique no link para redefinir a sua palavra passe <a href='http://127.0.0.1:5000/recuperar_password?token="+token+"'>Clique aqui</a>"
        mensagem=Message(assunto,sender="meu_email@gmail.com",recipients=[email_destino])
        mensagem.body=texto
        mensagem.html=texto
        mail.send(mensagem)
        return render_template("index.html",mensagem="Email de recuperação da palavra passe enviado.")
    else:
        #se o utilizador tem token (2º passo)
        #o pedido é um get
        if request.method=="GET":
            return render_template("utilizadores/recuperar_password.html",token=token,site_key=utilizadores.RECAPTCHA_SITE_KEY)
        else:
            #o utilizador tem token e o pedido é um post (3º passo)
            token=request.form.get("token")
            password=request.form.get("password")
            return utilizadores.Nova_Password(token,password)
            #return render_template("index.html",mensagem="Palavra passe alterada com sucesso.")

###


#logout
@app.route('/Logout')
def Logout():
    return utilizadores.Logout()




#Utilizadores
@app.route('/Utilizadores/info')
def Utilizadores_info():
    return render_template("Utilizadores/utilizadoresinfo.html")

@app.route("/Utilizadores/adicionar",methods=["POST","GET"])
def UtilizadorAdicionar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return utilizadores.Adicionar()

@app.route("/Utilizadores/listar")
def UtilizadorListar():
    if utilizadores.Logado()==False:
        return redirect("/")
    return utilizadores.Listar()

@app.route("/Utilizadores/perfil",methods=["POST","GET"])
def UtilizadoresPerfil():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return utilizadores.MudarPerfil()

@app.route("/Utilizadores/bloquear",methods=["POST","GET"])
def UtilizadorBloquear():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return utilizadores.Bloquear()

@app.route("/Utilizadores/editar",methods=["POST","GET"])
def UtilizadorEditar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return utilizadores.Editar()

@app.route("/Utilizadores/editar_confirmado",methods=["POST","GET"])
def UtilizadorEditarConfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return utilizadores.EditarConfirmado()

@app.route("/Utilizadores/apagar",methods=["POST","GET"])
def UtilizadorApagar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return utilizadores.Apagar()

@app.route("/Utilizadores/apagar_confirmado",methods=["POST","GET"])
def UtilizadorApagarConfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return utilizadores.ApagarConfirmado()


@app.route("/Perfil",methods=["GET"])
def EditarPerfil():
    if utilizadores.Logado()==False:
        return redirect("/")
    return utilizadores.EditarPerfil()

@app.route("/Utilizadores/perfil_confirmado",methods=["POST"])
def PerfilConfirmado():
    if utilizadores.Logado()==False:
        return redirect("/")
    return utilizadores.EditarConfirmado()

#########################################################


#-------------PARQUE-------------------------------
#rotas

@app.route('/parque/info')
def Parque_info():
    return render_template("parque/parqueinfo.html")

@app.route('/parque/adicionar',methods=["GET","POST"])
def parque_adicionar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return parque.parque_adicionar()

@app.route('/parque/listar')
def parque_listar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return parque.parque_listar()


@app.route('/parque/apagar',methods=["POST"])
def parque_apagar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return parque.parque_apagar()

@app.route('/parque/apagar_comfirmado',methods=["POST"])
def parque_apagar_comfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return parque.parque_apagar_comfirmado()

@app.route('/parque/editar',methods=["POST"])
def parque_editar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return parque.parque_editar()


@app.route('/parque/editar_comfirmado',methods=["POST"])
def parque_editar_comfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return parque.parque_editar_comfirmado()


@app.route('/parque/pesquisar/', methods=["POST","GET"])
def parque_pesquisar():
    return parque.parque_pesquisar()


#-------------VEICULO-------------------------------
@app.route('/veiculo/info')
def Veiculo_info():
    return render_template("veiculo/veiculoinfo.html")


@app.route('/veiculo/adicionar',methods=["GET","POST"])
def veiculo_adicionar():
    return veiculo.veiculo_adicionar(app)

@app.route('/veiculo/listar')
def veiculo_listar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return veiculo.veiculo_listar(app)

@app.route('/veiculo/apagar',methods=["POST"])
def veiculo_apagar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return veiculo.veiculo_apagar()

@app.route('/veiculo/apagar_comfirmado',methods=["POST"])
def veiculo_apagar_comfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return veiculo.veiculo_apagar_comfirmado()

@app.route('/veiculo/editar',methods=["POST"])
def veiculo_editar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return veiculo.veiculo_editar()

@app.route('/veiculo/editar_comfirmado',methods=["POST"])
def veiculo_editar_comfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return veiculo.veiculo_editar_comfirmado(app)

@app.route('/veiculo/pesquisar/', methods=["POST","GET"])
def veiculo_pesquisar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return veiculo.veiculo_pesquisar()


#-------------LUGAR-------------------------------
@app.route('/lugar/info')
def Lugar_info():
    return render_template("lugar/lugarinfo.html")

@app.route('/lugar/adicionar',methods=["GET","POST"])
def lugar_adicionar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return lugar.lugar_adicionar()

@app.route('/lugar/listar')
def lugar_listar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return lugar.lugar_listar()

@app.route('/lugar/apagar',methods=["POST"])
def lugar_apagar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return lugar.lugar_apagar()

@app.route('/lugar/apagar_comfirmado',methods=["POST"])
def lugar_apagar_comfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return lugar.lugar_apagar_comfirmado()

@app.route('/lugar/editar',methods=["POST"])
def lugar_editar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return lugar.lugar_editar()

@app.route('/lugar/editar_comfirmado',methods=["POST"])
def lugar_editar_comfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return lugar.lugar_editar_comfirmado()

#-------------ESTACIONAR-------------------------------
@app.route('/estacionar/info')
def Estacionar_info():
    return render_template("estacionar/estacionarinfo.html")

@app.route('/estacionar/adicionar',methods=["GET","POST"])
def estacionar_adicionar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return estacionar.estacionar_adicionar()

@app.route('/estacionar/listar')
def estacionar_listar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return estacionar.estacionar_listar()

@app.route('/estacionar/apagar',methods=["POST"])
def estacionar_apagar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return estacionar.estacionar_apagar()

@app.route('/estacionar/apagar_comfirmado',methods=["POST"])
def estacionar_apagar_comfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return estacionar.estacionar_apagar_comfirmado()

@app.route('/estacionar/editar',methods=["POST"])
def estacionar_editar():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return estacionar.estacionar_editar()

@app.route('/estacionar/editar_comfirmado',methods=["POST"])
def estacionar_editar_comfirmado():
    if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
        return redirect("/")
    return estacionar.estacionar_editar_comfirmado()


@app.errorhandler(404)
def erro_404(evento):
    return render_template("/404/404.html")




if __name__ == "__main__":
    app.run(debug=True)