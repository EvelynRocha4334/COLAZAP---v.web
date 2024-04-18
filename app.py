from flask import Flask, render_template , request, redirect, session, jsonify, url_for 
from usuario import Usuario
from contato import Contato  
from chat import Chat

app = Flask(__name__)

app.secret_key = "vivizinha"

@app.route("/", methods=["GET","POST"]) 
def cadastro():
    if request.method == 'GET':
        return render_template("cadastro.html")
    else:
        usuario = Usuario()         
        nome = request.form["nome"]
        tel = request.form["telefone"]
        senha = request.form["senha"]

        if usuario.cadastrar(nome, tel, senha) == True:
            print(f"Cadastro efetuado com sucesso! Seja Bem-Vindo!")
        else:
            print("Não foi possível concluir seu cadastro!")
        return render_template("cadastro.html")


@app.route("/login" , methods=["POST", "GET"])
def pagina_login():
   if request.method == 'GET':
        return render_template("login.html")
   else:
        telefone = request.form["telefone"]
        senha = request.form["senha"]
        usuario= Usuario()
        usuario.logar(telefone,senha)
        if usuario.logado == True:
            session['usuario_logado'] =  {"nome": usuario.nome,
                                            "telefone": usuario.telefone}
            return redirect("/chat")
        else:
            return redirect("/login")
        


@app.route("/retorna_usuarios")
def retorna_usuarios():
    nome_usuario = session ["usuario_logado"]["nome"]
    telefone_usuario = session ["usuario_logado"]["telefone"]
    chat =  Chat(nome_usuario,telefone_usuario)

    contatos = chat.retornar_contatos()
    return jsonify(contatos), 200
    

@app.route("/chat")
def pag_chat():
    if "usuario_logado" in session:
        return render_template("chat.html")
    else:
        return redirect("/login") 




@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    nome_usuario = session ["usuario_logado"]["nome"]
    telefone_usuario = session ["usuario_logado"]["telefone"]
    chat =  Chat(nome_usuario,telefone_usuario)

    destinatario = Contato("", tel_destinatario)

    mensagens = chat.verificar_mensagem(0, destinatario)

    return jsonify(mensagens), 200 


@app.route("/enviar_mensagem", methods=['GET', 'POST'])
def enviar_mensagem():
    dados = request.get_json()
    
    nome_usuario = session['usuario_logado']["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    destinatario = dados["usuario"]
    mensagem = dados["mensagem"]

    chat = Chat(nome_usuario, telefone_usuario)
    contato = Contato("", destinatario)
    mensagens = chat.enviar_mensagem(mensagem, contato)
    return jsonify(mensagens), 200


app.run(host='0.0.0.0',port='8080')












# @app.route("/login", methods=["GET", "POST"])
# def pagina_login():
#     if request.method == 'GET':
#         return render_template("login.html")
#     else:
#         usuario = Usuario()
#         tel = request.form["tel"]
#         senha = request.form["senha"]

#         usuario.logar(tel, senha)

#         if usuario.logado == True:
#             return render_template("chat.html")

#         if not usuario.logado:
#             print("Usuário ou senha inválidos!")
#         return render_template("login.html")





# @app.route("/enviar_mensagem", methods=['GET', 'POST'])
# def enviar_mensagem():
#     dados = request.get_json()
    
#     nome_usuario = session['usuario_logado']["nome"]
#     telefone_usuario = session["usuario_logado"]["telefone"]

#     destinatario = dados["tel"]
#     mensagem = dados["mensagem"]

#     chat = Chat(nome_usuario, telefone_usuario)
#     contato = Contato("", destinatario)
#     mensagens = chat.enviar_mensagem(mensagem, contato)
#     return jsonify(mensagens), 200










# @app.route("/chat")
    
# @app.route("/cadastrar_via_ajax", methods = ["POST"])
# def post_cadastro_ajax():
#     dados = request.get_json()
#     nome = dados["nome"]
#     tel = dados["telefone"]
#     senha = dados["senha"]

#     usuario = Usuario() 

#     if usuario.cadastrar(tel, nome, senha) == True:
#             return jsonfy({'mensagem:' : 'Cadastro OK'}),200
#     else:
#         return jsonfy({'mensagem' : 'ERRO'}), 500



app.run(debug=True)