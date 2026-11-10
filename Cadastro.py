import sqlite3

banco = sqlite3.connect("clientes.db")
cursor = banco.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS clientes (nome TEXT, telefone TEXT, cidade TEXT)")
banco.commit()

print("=== SISTEMA DE CADASTRO - ADS ===")

while True:
    print("1 - cadastrar clientes")
    print("2 - Listar clientes")
    print("3 - busca clientes")
    print("4 - sair")
    print("5 - contar clientes")
    print("6 - Excluir clientes")
    print("7 - Atualizar clientes")
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
        busca = input("Digite o nome pra buscar: ")
        cursor.execute("SELECT * FROM clientes WHERE nome LIKE ?", ("%" + busca + "%",))
        achados = cursor.fetchall()
        if achados:
            for cliente in achados:
                print(cliente)
        else:
            print("Nenhum cliente encontrado.")

    elif opcao == "4":
        break
    elif opcao == "5":
    	cursor.execute("SELECT  COUNT(*) FROM clientes")
    	total = cursor.fetchone()[0]
    	print(f"Total de clientes cadastrados:  {total}")
    elif opcao == "6":
    	nome_excluir = input("Digite o nome pra excluir: ").strip()
    	cursor.execute(f"DELETE FROM clientes WHERE nome LIKE '%{nome_excluir}%'")
    	print("Apagados:", cursor.rowcount)
    	banco.commit()
    	print("Cliente excluido!")
    elif opcao == "7":
    	nome_atualizar  =  input("Digite o nome que quer atualizar:  ").strip()
    	novo_telefone  =  input("Digite o novo telefone:  ").strip()
    	nova_cidade  =  input("Digite a nova cidade:  ").strip()
    	
    	cursor.execute(f"UPDATE clientes SET telefone  =  ' {novo_telefone} ' , cidade  =  ' {nova_cidade} '  WHERE nome LIKE '%{nome_atualizar}%' ")
    	print("Atualizados:" , cursor.rowcount)
    	banco.commit()
    	print("Cliente atualizado!")
    else:
           print("opcao invalida!")