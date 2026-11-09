import sqlite3

banco = sqlite3.connect("clientes.db")
cursor = banco.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS clientes (nome TEXT, telefone TEXT, cidade TEXT)")
banco.commit()

print("=== SISTEMA DE CADASTRO - ADS ===")

while True:
    print("1 - cadastrar clientes")
    print("2 - Listar clientes")
    print("3 - Sair")
    opcao = input("escolha: ")

    if opcao == "1":
        nome = input("Nome: ")
        telefone = input("Telefone: ")
        cidade = input("Cidade: ")
        cursor.execute("INSERT INTO clientes VALUES (?, ?, ?)", (nome, telefone, cidade))
        banco.commit()
        print("Cliente cadastrado!")

    elif opcao == "2":
        cursor.execute("SELECT * FROM clientes")
        for cliente in cursor.fetchall():
            print(cliente)

    elif opcao == "3":
        break

    else:
        print("opcao invalida!")