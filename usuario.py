from conexao import Conexao
from hashlib import sha256


class Usuario():
    def __init__(self) -> None:
        self.nome = None
        self.telefone = None
        self.senha = None
        self.logado = False   #boolean (false ou true)

    def cadastrar (self,nome,telefone,senha):
        try:

            # Criptografando a senha
            senha = sha256(senha.encode()).hexdigest()

            # Conectando no banco de dados
            mydb =  Conexao.conectar()

            mycursor = mydb.cursor()

            sql = "INSERT INTO tb_usuario (nome, tel, senha) VALUES (%s, %s, %s)"
            val = (nome, telefone, senha)
            mycursor.execute(sql, val)

            mydb.commit()

            self.nome = nome 
            self.telefone = telefone
            self.senha = senha
            self.logado = True 

            return True
        
        except:
            return False



    def logar(self,telefone,senha):

        # Criptografando a senha
        senha = sha256(senha.encode()).hexdigest()

        mydb =  Conexao.conectar()

        mycursor = mydb.cursor()

        # Forma 1
        # sql = f"SELECT * FROM tb_usuario WHERE tel = '{telefone}' and senha = '{senha}';"

        # Forma 2
        sql = "SELECT nome,tel,senha FROM tb_usuario WHERE tel = %s and BINARY senha = %s;"
        valores = (telefone,senha)
        mycursor.execute(sql,valores)
        

        resultado = mycursor.fetchone()

        if resultado != None:
            self.logado = True 
            self.nome = resultado [0]
            self.telefone = resultado [1]
            self.senha = resultado [2]

        else: self.logado = False

    




    