from os import system
from colorama import init, Fore # nescecita instalar
from getpass import getpass
import stdiomask # nescecita instalar
from time import sleep
import psycopg2 as db

init(autoreset=True)

# Criando o menu de opções

def exibir_menu():
    print(Fore.GREEN + '''Bem-vindo(a) ao projeto
        Sistema de Login
    Escolha uma opção:
    [1] Cadastrar novo usuário
    [2] Fazer Login
    [3] Sair
    ''')

    opcao = int(input('Digite sua opção: '))
    return(opcao)

def menu_professor():
    print(Fore.GREEN + '''Bem-vindo(a) professor(a)
    Escolha uma opção:
    [1] Ver alunos
    [2] Cadastrar novo Aluno
    [3] Inserir notas
    [4] Ver notas dos alunos
    [5] Editar notas
    ''')

    opcao = int(input('Digite sua opção: '))
    return(opcao)


# Fazer login com nome e senha de usuario

def fazer_login():
    login = input('Nome: ')
    senha = stdiomask.getpass(prompt='Senha: ', mask='')
    return(login,senha)


def fazer_cadastro():
    status = int(input('Digite [1] = Professor ou [2] = Aluno. '))
    login = input('Nome: ')
    senha = stdiomask.getpass(prompt='Senha: ', mask='')
    return(login,senha,status)

class Config:
    def __init__(self):
        self.config = {
            "postgres": {
                "user": "postgres",
                "password": "321654987",
                "host": "localhost",
                "database": "db_arch"
            }
        }

class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        try:
            self.conn = db.connect(**self.config["postgres"])
            self.cur = self.conn.cursor()
        except Exception as ex:
            print("Erro na conexão ", ex)
            exit(1)

    def __enter__(self):
        return self

    def __exit__(self):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

class Crud(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, table, fields, args):
        try:
            sql = "INSERT INTO "+table+" ("+fields+") VALUES ("+args+")"
            self.execute(sql, args)
            self.commit()
        except Exception as ex:
            print("Erro ao inserir: ", ex)

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM users WHERE id_user = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar"
            sql_d = f"DELETE FROM users WHERE id_user = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as ex:
            print("Erro ao deletar: ", ex)

    def update(self, table, id, fields, column, args):
        try:
            sql_s = f"SELECT * FROM users WHERE id_user = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para atualizar"
            sql = f"UPDATE {table} SET ({fields}) = ({args}) WHERE {column} = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado!")
        except Exception as ex:
            print("Erro ao atualizar: ", ex)

    def search(self, *args, type_s="nome_user"):
        sql = "SELECT * FROM users WHERE nome_user = %s"
        if type_s == "id_user":
            sql = "SELECT * FROM users WHERE id_user = %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"

    def read_professor(self):
        sql = "SELECT * FROM users WHERE status = 'Aluno'"
        data = self.query(sql)
        if data:
            return data
        return "Registro não encontrado"

while True:
    system('cls')
    opcao = exibir_menu()

    if opcao == 1:
        # Cadastrar novo usuário
        login, senha, status = fazer_cadastro()
        if login == senha:
            print('Sua senha deve ser diferente do login.')
            senha = getpass('Senha: ')

        buscador = Crud()
        #print(buscador.search(login))
        
        user = buscador.search(login)
        if user != "Registro não encontrado":
            for row in user:
                id = row[0]
                nome = row[1]
                status = row[3]
            # user = buscar_usuario(login, senha)
            if nome == login:
                print(Fore.RED+'Usuário já existente!')
                sleep(2)
                #exit()
        else:
            inserindo = Crud()
            if status == 1:
                status = "Professor"
            elif status == 2:
                status = "Aluno"
            fields = "nome_user, password, status"
            argum = "'{}','{}','{}'".format(login, senha, status)
            inserindo.insert("users",fields, argum)
            print(inserindo.query("SELECT * FROM users"))
            print(Fore.CYAN + 'Cadastro aprovado!')
            exit()

    elif opcao == 2:
        # Fazer o login do usuário
        login, senha = fazer_login()

        buscador = Crud()
        user = buscador.search(login)
        if user != "Registro não encontrado":
            for row in user:
                id = row[0]
                nome = row[1]
                status = row[3]
            if nome == login:
                print(Fore.CYAN + 'lOGIN REALIZADO COM SUCESSO! Seja bem vindo '+status)
                sleep(1)
                if status == "Professor":
                    


                    # API do professor
                    opcao = menu_professor()

                    if opcao == 1:
                        # Ver lista de alunos
                        buscador = Crud()
                        #print(buscador.search(login))
                        
                        alunos = buscador.read_professor()
                        for aluno in alunos:
                            print(aluno)
                        sleep(2)
                        exit()

                    elif opcao == 2:
                        # Inserir novo Aluno
                        inserindo = Crud()
                        fields = "nome_user, password, status"
                        nome = input('Nome do aluno: ')
                        argum = "'{}', 'admin', 'Aluno'".format(nome)
                        inserindo.insert("users",fields, argum)
                        print(inserindo.query("SELECT * FROM users WHERE status = 'Aluno'"))
                        print(Fore.CYAN + 'Cadastro de aluno realizado com sucesso!')
                        sleep(2)
                        exit()
                    
                    elif opcao == 3:
                        # Inserir notas de um aluno especifico
                        crud = Crud()
                        print(crud.query("SELECT * FROM users WHERE status = 'Aluno'"))
                        id = int(input('Escolha um aluno pelo ID: '))
                        n1 = int(input('Primeira nota: '))
                        n2 = int(input('Segunda nota: '))
                        n3 = int(input('Terceira nota: '))
                        n4 = int(input('Quarta nota: '))
                        
                        # Formando a query
                        fields = "aluno_id, n1, n2, n3, n4"
                        argum = "'{}','{}','{}','{}','{}'".format(id, n1, n2, n3, n4)
                        # Inserindo no banco
                        crud.insert("notas",fields, argum)
                        
                        #print(crud.query("SELECT * FROM notas"))
                        id = str(id)
                        print(crud.query("SELECT (nome_user, n1, n2, n3, n4) FROM notas INNER JOIN users ON users.id_user = notas.aluno_id WHERE aluno_id = '"+id+"'"))
                        print(Fore.CYAN + 'Notas inseridas corretamente!')
                        sleep(2)
                        notas = crud.query("SELECT * FROM notas WHERE aluno_id = '"+id+"'")
                        for nota in notas:
                            n1 = nota[2] 
                            n2 = nota[3]
                            n3 = nota[4]
                            n4 = nota[5]
                        media = (n1 + n2 + n3 + n4)/4
                        media_str = str(media)
                        if media < 4:
                            print("Aluno reprovado com media: "+media_str)
                        elif media >= 4 and media < 6:
                            print("Aluno em recuperação com media: "+media_str)
                        elif media >= 6:
                            print("Aluno aprovado com media: "+media_str)
                        sleep(2)
                        exit()

                    elif opcao == 4:
                    #Ver notas dos alunos
                        crud  = Crud()
                        print(crud.query("SELECT (nome_user, n1, n2, n3, n4) FROM notas INNER JOIN users ON users.id_user = notas.aluno_id"))
                        notas = crud.query("SELECT * FROM notas")
                        #print(len(notas))
                        for nota in notas:
                            id = nota[1]
                            n1 = nota[2] 
                            n2 = nota[3]
                            n3 = nota[4]
                            n4 = nota[5]
                            id = str(id)
                            nome = crud.query("SELECT (nome_user) FROM notas INNER JOIN users ON users.id_user = notas.aluno_id WHERE aluno_id = '"+id+"'")
                            media = (n1 + n2 + n3 + n4)/4
                            
                            nome_str = str(nome)
                            media_str = str(media)

                            if media < 4:
                                print("Aluno "+nome_str+" reprovado com media: "+media_str)
                            elif media >= 4 and media < 6:
                                print("Aluno "+nome_str+" em recuperação com media: "+media_str)
                            elif media >= 6:
                                print("Aluno "+nome_str+" aprovado com media: "+media_str)
                        sleep(2)
                        exit()

                    elif opcao == 5:
                        # Editar notas de um aluno especifico
                        crud  = Crud()
                        print(crud.query("SELECT (nome_user, n1, n2, n3, n4) FROM notas INNER JOIN users ON users.id_user = notas.aluno_id"))
                        notas = crud.query("SELECT * FROM notas")
                        #print(len(notas))
                        for nota in notas:
                            id = nota[1]
                            n1 = nota[2] 
                            n2 = nota[3]
                            n3 = nota[4]
                            n4 = nota[5]
                            id = str(id)
                            nome = crud.query("SELECT (nome_user) FROM notas INNER JOIN users ON users.id_user = notas.aluno_id WHERE aluno_id = '"+id+"'")
                            media = (n1 + n2 + n3 + n4)/4
                            
                            nome_str = str(nome)
                            media_str = str(media)

                            if media < 4:
                                print("Aluno "+nome_str+" reprovado com media: "+media_str)
                            elif media >= 4 and media < 6:
                                print("Aluno "+nome_str+" em recuperação com media: "+media_str)
                            elif media >= 6:
                                print("Aluno "+nome_str+" aprovado com media: "+media_str)
                        print(crud.query("SELECT (id_user, nome_user) FROM users WHERE status = 'Aluno'"))
                        id = int(input('Escolha um aluno pelo ID: '))
                        n1 = int(input('Editar Primeira nota: '))
                        n2 = int(input('Editar Segunda nota: '))
                        n3 = int(input('Editar Terceira nota: '))
                        n4 = int(input('Editar Quarta nota: '))
                        
                        # Formando a query
                        fields = " n1, n2, n3, n4"
                        argum = "'{}','{}','{}','{}'".format(n1, n2, n3, n4)
                        # Inserindo no banco
                        crud.update("notas",id,fields, "aluno_id", argum)
                        id_str = str(id)
                        notas = crud.query("SELECT * FROM notas WHERE aluno_id = '"+id_str+"'")
                        #print(len(notas))
                        for nota in notas:
                            n1 = nota[2] 
                            n2 = nota[3]
                            n3 = nota[4]
                            n4 = nota[5]
                            id = str(id)
                            nome = crud.query("SELECT (nome_user) FROM notas INNER JOIN users ON users.id_user = notas.aluno_id WHERE aluno_id = '"+id+"'")
                            media = (n1 + n2 + n3 + n4)/4
                            
                            nome_str = str(nome)
                            media_str = str(media)

                            if media < 4:
                                print("Aluno "+nome_str+" reprovado com media: "+media_str)
                            elif media >= 4 and media < 6:
                                print("Aluno "+nome_str+" em recuperação com media: "+media_str)
                            elif media >= 6:
                                print("Aluno "+nome_str+" aprovado com media: "+media_str)
                        sleep(2)
                        exit()

                else:
                    crud = Crud()
                    id = str(id)
                    print(crud.query("SELECT (nome_user, n1, n2, n3, n4) FROM notas INNER JOIN users ON users.id_user = notas.aluno_id WHERE aluno_id = '"+id+"'"))
                    sleep(2)
                    notas = crud.query("SELECT * FROM notas WHERE aluno_id = '"+id+"'")
                    for nota in notas:
                        n1 = nota[2] 
                        n2 = nota[3]
                        n3 = nota[4]
                        n4 = nota[5]
                    media = (n1 + n2 + n3 + n4)/4
                    nome_str = str(nome)
                    media_str = str(media)

                    if media < 4:
                        print("Aluno "+nome_str+" reprovado com media: "+media_str)
                    elif media >= 4 and media < 6:
                        print("Aluno "+nome_str+" em recuperação com media: "+media_str)
                    elif media >= 6:
                        print("Aluno "+nome_str+" aprovado com media: "+media_str)
                    sleep(2)
                    exit()

        else:
            print(Fore.RED + 'Você deve ter digitado seu nome de usuário ou a senha errado. \n Por favor verifique novamente.')
            sleep(2)

    elif opcao == 3:
        system('cls')
        print(Fore.LIGHTMAGENTA_EX + 'GoodBay!')
        break
    
    else:
        print(Fore.RED+'Você deve ter digitado algum comando errado. \n Por favor verifique novamente.')
        sleep(2)
        # exit()