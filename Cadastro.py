import sqlite3

banco = sqlite3.connect("clientes.db")
cursor = banco.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS clientes (nome TEXT, telefone TEXT, cidade TEXT)")
banco.commit()

while True:
    # Cabeçalho Principal Organizado com Linhas Estilizadas
    print("\n" + "="*40)
    print("      SISTEMA DE CADASTRO - ADS")
    print("="*40)
    print(" [1] Cadastrar Cliente")
    print(" [2] Listar Todos os Clientes")
    print(" [3] Buscar Cliente por Nome")
    print(" [5] Contar Total de Registros")
    print(" [6] Excluir Registro")
    print(" [7] Atualizar Informacoes")
    print(" [4] Sair do Sistema")
    print("-"*40)
    
    opcao = input(" Escolha uma opcao: ").strip()
    print("-"*40)

    if opcao == "1":
        print(" >>> NOVO CADASTRO <<<")
        nome = input(" Nome: ")
        telefone = input(" Telefone: ")
        cidade = input(" Cidade: ")
        
        cursor.execute("INSERT INTO clientes VALUES (?, ?, ?)", (nome, telefone, cidade))
        banco.commit()
        print("-"*40)
        print(" STATUS: Registro salvo com sucesso.")

    elif opcao == "2":
        print(" >>> LISTA DE CLIENTES CADASTRADOS <<<")
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        
        if clientes:
            # Cabeçalho de colunas alinhado
            print(f" {'NOME':<15} | {'TELEFONE':<12} | {'CIDADE':<15}")
            print("-"*50)
            for cliente in clientes:
                print(f" {cliente[0]:<15} | {cliente[1]:<12} | {cliente[2]:<15}")
        else:
            print(" STATUS: Banco de dados vazio.")

    elif opcao == "3":
        print(" >>> BUSCA DE REGISTROS <<<")
        busca = input(" Digite o nome para buscar: ")
        cursor.execute("SELECT * FROM clientes WHERE nome LIKE ?", ("%" + busca + "%",))
        achados = cursor.fetchall()
        
        print("-"*40)
        if achados:
            print(f" {'NOME':<15} | {'TELEFONE':<12} | {'CIDADE':<15}")
            print("-"*50)
            for cliente in achados:
                print(f" {cliente[0]:<15} | {cliente[1]:<12} | {cliente[2]:<15}")
        else:
            print(" STATUS: Nenhum resultado encontrado.")

    elif opcao == "4":
        print(" Encerrando sessao de forma segura...")
        break
        
    elif opcao == "5":
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total = cursor.fetchone()[0]
        print(f" STATUS: Total de registros ativos: {total}")
        
    elif opcao == "6":
        print(" >>> EXCLUSÃO DE REGISTRO <<<")
        nome_excluir = input(" Digite o nome para remover: ").strip()
        
        print("-"*40)
        if nome_excluir == "":
            print(" ERRO: Entrada invalida. Operacao abortada.")
        else:
            cursor.execute("DELETE FROM clientes WHERE nome LIKE ?", ("%" + nome_excluir + "%",))
            banco.commit()
            if cursor.rowcount > 0:
                print(f" STATUS: {cursor.rowcount} registro(s) removido(s).")
            else:
                print(" STATUS: Nenhum registro correspondente encontrado.")
            
    elif opcao == "7":
        print(" >>> ATUALIZAÇÃO DE DADOS <<<")
        nome_atualizar = input(" Digite o nome para modificar: ").strip()
        
        print("-"*40)
        if nome_atualizar == "":
            print(" ERRO: Entrada invalida. Operacao abortada.")
        else:
            novo_telefone = input(" Digite o novo telefone: ").strip()
            nova_cidade = input(" Digite a nova cidade: ").strip()
            
            cursor.execute(
                "UPDATE clientes SET telefone = ?, cidade = ? WHERE nome LIKE ?", 
                (novo_telefone, nova_cidade, "%" + nome_atualizar + "%")
            )
            banco.commit()
            print("-"*40)
            if cursor.rowcount > 0:
                print(f" STATUS: {cursor.rowcount} registro(s) atualizado(s).")
            else:
                print(" STATUS: Nenhum registro correspondente encontrado.")
            
    else:
        print(" ERRO: Opcao invalida no menu.")

banco.close()
