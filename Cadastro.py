import sqlite3

try:
    banco = sqlite3.connect("clientes.db")
    cursor = banco.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS clientes (nome TEXT, telefone TEXT, cidade TEXT)")
    banco.commit()
except sqlite3.Error as e:
    print(f" ERRO CRITICO DE BANCO DE DADOS: {e}")
    exit()

RESET = "\033[0m"
TEXT_ERRO = "\033[91m"
TEXT_STATUS = "\033[92m"

TEMAS = {
    "1": {"nome_tema": "Azul Profissional", "bg_cabecalho": "\033[44m", "text_cabecalho": "\033[97m", "text_botao": "\033[94m"},
    "2": {"nome_tema": "Verde Suave", "bg_cabecalho": "\033[42m", "text_cabecalho": "\033[97m", "text_botao": "\033[96m"},
    "3": {"nome_tema": "Grafite + Laranja Suave", "bg_cabecalho": "\033[100m", "text_cabecalho": "\033[97m", "text_botao": "\033[93m"},
    "4": {"nome_tema": "Modo Escuro Total", "bg_cabecalho": "\033[40m", "text_cabecalho": "\033[37m", "text_botao": "\033[90m"}
}

BG_CABECALHO = TEMAS["4"]["bg_cabecalho"]
TEXT_BRANCO = TEMAS["4"]["text_cabecalho"]
TEXT_BOTAO = TEMAS["4"]["text_botao"]

def gerar_pdf_relatorio(dados_clientes, termo_busca):
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "SISTEMA DE CADASTRO - ADS", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(190, 10, f"Filtro de Busca por: '{termo_busca}'", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(60, 10, "Nome", border=1)
        pdf.cell(50, 10, "Telefone", border=1)
        pdf.cell(80, 10, "Cidade", border=1)
        pdf.ln()
        pdf.set_font("Arial", "", 10)
        for cliente in dados_clientes:
            pdf.cell(60, 10, str(cliente[0]), border=1)
            pdf.cell(50, 10, str(cliente[1]), border=1)
            pdf.cell(80, 10, str(cliente[2]), border=1)
            pdf.ln()
        nome_arquivo = f"relatorio_busca_{termo_busca.replace(' ', '_')}.pdf"
        pdf.output(nome_arquivo)
        print(f" {TEXT_STATUS}STATUS: PDF '{nome_arquivo}' gerado com sucesso.{RESET}")
    except ImportError:
        print(f" {TEXT_ERRO}ERRO: Biblioteca fpdf2 nao encontrada. Va no menu PIP do Pydroid 3 e instale 'fpdf2'.{RESET}")
    except Exception as err:
        print(f" {TEXT_ERRO}ERRO AO GERAR PDF: {err}{RESET}")

while True:
    print(f"\n{BG_CABECALHO}{TEXT_BRANCO}{'='*40}{RESET}")
    print(f"{BG_CABECALHO}{TEXT_BRANCO}      SISTEMA DE CADASTRO - ADS         {RESET}")
    print(f"{BG_CABECALHO}{TEXT_BRANCO}{'='*40}{RESET}")
    print(f" [{TEXT_BOTAO}1{RESET}] Cadastrar Cliente")
    print(f" [{TEXT_BOTAO}2{RESET}] Listar Todos os Clientes")
    print(f" [{TEXT_BOTAO}3{RESET}] Buscar Cliente por Nome (com opcao de PDF)")
    print(f" [{TEXT_BOTAO}4{RESET}] Sair do Sistema")
    print(f" [{TEXT_BOTAO}5{RESET}] Contar Total de Registros")
    print(f" [{TEXT_BOTAO}6{RESET}] Excluir Registro")
    print(f" [{TEXT_BOTAO}7{RESET}] Atualizar Informacoes")
    print(f" [{TEXT_BOTAO}8{RESET}] Mudar Layout / Modo Escuro")
    print("-"*40)
    opcao = input(" Escolha uma opcao: ").strip()
    print("-"*40)
    try:
        if opcao == "1":
            print(f" {TEXT_BOTAO}>>> NOVO CADASTRO <<<{RESET}")
            while True:
                nome = input(" Nome: ").strip()
                if nome == "":
                    print(f" {TEXT_ERRO}ERRO: O campo nome nao pode ficar vazio.{RESET}")
                else:
                    break
            while True:
                telefone = input(" Telefone: ").strip()
                if telefone == "":
                    print(f" {TEXT_ERRO}ERRO: O campo telefone nao pode ficar vazio.{RESET}")
                else:
                    break
            while True:
                cidade = input(" Cidade: ").strip()
                if cidade == "":
                    print(f" {TEXT_ERRO}ERRO: O campo cidade nao pode ficar vazio.{RESET}")
                else:
                    break
            cursor.execute("INSERT INTO clientes VALUES (?, ?, ?)", (nome, telefone, cidade))
            banco.commit()
            print("-"*40)
            print(f" {TEXT_STATUS}STATUS: Registro salvo com sucesso.{RESET}")
        elif opcao == "2":
            print(f" {TEXT_BOTAO}>>> LISTA DE CLIENTES CADASTRADOS <<<{RESET}")
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()
            if clientes:
                print(f" {'NOME':<15} | {'TELEFONE':<12} | {'CIDADE':<15}")
                print("-"*50)
                for cliente in clientes:
                    print(f" {cliente[0]:<15} | {cliente[1]:<12} | {cliente[2]:<15}")
            else:
                print(f" {TEXT_ERRO}STATUS: Banco de dados vazio.{RESET}")
        elif opcao == "3":
            print(f" {TEXT_BOTAO}>>> BUSCA DE REGISTROS <<<{RESET}")
            while True:
                busca = input(" Digite o nome para buscar: ").strip()
                if busca == "":
                    print(f" {TEXT_ERRO}ERRO: O termo de busca nao pode ser vazio.{RESET}")
                else:
                    break
            cursor.execute("SELECT * FROM clientes WHERE nome LIKE ?", ("%" + busca + "%",))
            achados = cursor.fetchall()
            print("-"*40)
            if achados:
                print(f" {'NOME':<15} | {'TELEFONE':<12} | {'CIDADE':<15}")
                print("-"*50)
                for cliente in achados:
                    print(f" {cliente[0]:<15} | {cliente[1]:<12} | {cliente[2]:<15}")
                print("-"*40)
                exportar = input(" Deseja exportar este resultado de busca em PDF? (s/n): ").strip().lower()
                if exportar == "s":
                    gerar_pdf_relatorio(achados, busca)
            else:
                print(f" {TEXT_ERRO}STATUS: Nenhum resultado encontrado.{RESET}")
        elif opcao == "4":
            print(" Encerrando sessao de forma segura...")
            break
        elif opcao == "5":
            cursor.execute("SELECT COUNT(*) FROM clientes")
            total = cursor.fetchone()[0]
            print(f" {TEXT_STATUS}STATUS: Total de registros ativos: {total}{RESET}")
        elif opcao == "6":
            print(f" {TEXT_BOTAO}>>> EXCLUSÃO DE REGISTRO <<<{RESET}")
            while True:
                nome_excluir = input(" Digite o nome para remover: ").strip()
                if nome_excluir == "":
                    print(f" {TEXT_ERRO}ERRO: O campo de exclusao nao pode ser vazio.{RESET}")
                else:
                    break
            print("-"*40)
            cursor.execute("DELETE FROM clientes WHERE nome LIKE ?", ("%" + nome_excluir + "%",))
            banco.commit()
            if cursor.rowcount > 0:
                print(f" {TEXT_STATUS}STATUS: {cursor.rowcount} registro(s) removido(s).{RESET}")
            else:
                print(f" {TEXT_ERRO}STATUS: Nenhum registro correspondente encontrado.{RESET}")
        elif opcao == "7":
            print(f" {TEXT_BOTAO}>>> ATUALIZAÇÃO DE DADOS <<<{RESET}")
            while True:
                nome_atualizar = input(" Digite o nome para modificar: ").strip()
                if nome_atualizar == "":
                    print(f" {TEXT_ERRO}ERRO: O nome de busca nao pode ser vazio.{RESET}")
                else:
                    break
            print("-"*40)
            while True:
                novo_telefone = input(" Digite o novo telefone: ").strip()
                if novo_telefone == "":
                    print(f" {TEXT_ERRO}ERRO: O campo telefone nao pode ficar vazio.{RESET}")
                else:
                    break
            while True:
                nova_cidade = input(" Digite a nova cidade: ").strip()
                if nova_cidade == "":
                    print(f" {TEXT_ERRO}ERRO: O campo cidade nao pode ficar vazio.{RESET}")
                else:
                    break
            cursor.execute("UPDATE clientes SET telefone = ?, cidade = ? WHERE nome LIKE ?", (novo_telefone, nova_cidade, "%" + nome_atualizar + "%"))
            banco.commit()
            print("-"*40)
            if cursor.rowcount > 0:
                print(f" {TEXT_STATUS}STATUS: {cursor.rowcount} registro(s) atualizado(s).{RESET}")
            else:
                print(f" {TEXT_ERRO}STATUS: Nenhum registro correspondente encontrado.{RESET}")
        elif opcao == "8":
            print(f" {TEXT_BOTAO}>>> AJUSTE DE LAYOUT <<<{RESET}")
            print(" 1 - Azul Profissional")
            print(" 2 - Verde Suave")
            print(" 3 - Grafite + Laranja Suave")
            print(" 4 - Modo Escuro Total")
            print("-"*40)
            troca = input(" Escolha o novo tema visual: ").strip()
            if troca in TEMAS:
                BG_CABECALHO = TEMAS[troca]["bg_cabecalho"]
                TEXT_BRANCO = TEMAS[troca]["text_cabecalho"]
                TEXT_BOTAO = TEMAS[troca]["text_botao"]
                print(f" {TEXT_STATUS}STATUS: Tema alterado para '{TEMAS[troca]['nome_tema']}'.{RESET}")
            else:
                print(f" {TEXT_ERRO}ERRO: Escolha invalida. Mantendo o tema atual.{RESET}")
        else:
            print(f" {TEXT_ERRO}ERRO: Opcao invalida no menu.{RESET}")
    except sqlite3.Error as erro_sql:
        print(f" {TEXT_ERRO}ERRO OPERACIONAL NO BANCO: {erro_sql}{RESET}")

banco.close()
print(" Conexao encerrada com segurança.")
