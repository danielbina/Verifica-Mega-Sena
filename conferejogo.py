import mysql.connector

# Função para conectar ao banco de dados
# Retorna um objeto de conexão

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",  
        user="root",  
        password="",  
        database="megasena"  
    )

# Função para criar a tabela de jogos se não existir

def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jogos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numeros VARCHAR(255) NOT NULL
        )
        """
    )
    conexao.close()

# Função para cadastrar um novo jogo

def cadastrar_jogo():
    print("Cadastro de Novo Jogo")
    while True:
        try:
            qtd_numeros = int(input("Quantos números terá o jogo? (6, 7 ou 8): "))
            
            if qtd_numeros not in [6, 7, 8]:
                print("Quantidade inválida! Escolha entre 6, 7 ou 8.")
                continue
            
            break
        except ValueError:
            print("Por favor, insira um número válido.")
    
    while True:
        try:
            numeros = input(f"Digite os {qtd_numeros} números do jogo separados por vírgula: ").strip()
            numeros = list(map(int, numeros.split(",")))
            
            if len(numeros) != qtd_numeros:
                print("A quantidade de números deve ser igual ao escolhido.")
                continue
            
            for n in numeros:
                if n < 1 or n > 60:
                    print("Os números devem estar entre 1 e 60.")
                    continue
            
            break
        except ValueError:
            print("Por favor, insira apenas números separados por vírgula.")
    
    # Conecta ao banco e insere os números
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO jogos (numeros) VALUES (%s)", (" ".join(map(str, numeros)),))
    conexao.commit()
    conexao.close()
    print("Jogo cadastrado com sucesso!")

# Função para deletar um jogo do banco

def deletar_jogo():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id, numeros FROM jogos")
    jogos = cursor.fetchall()
    conexao.close()
    
    if not jogos:
        print("Nenhum jogo cadastrado ainda!")
        return
    
    for jogo in jogos:
        id_jogo, numeros = jogo
        print(f"ID: {id_jogo} - Números: {numeros}")
    
    try:
        id_jogo = int(input("\nDigite o ID do jogo que deseja deletar ou 0 para sair: "))
        
        if id_jogo == 0:
            return
        
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM jogos WHERE id = %s", (id_jogo,))
        conexao.commit()
        conexao.close()
        print("Jogo deletado com sucesso!")
    except ValueError:
        print("Por favor, insira um ID válido.")

# Função para verificar quais jogos acertaram os números sorteados

def verificar_jogos():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, numeros FROM jogos")
    jogos = cursor.fetchall()
    conexao.close()
    
    if not jogos:
        print("Nenhum jogo cadastrado ainda!")
        return
    
    try:
        sorteados = input("Digite os números sorteados separados por vírgula: ").strip()
        sorteados = list(map(int, sorteados.split(",")))
        
        if len(sorteados) != 6:
            print("Os números sorteados devem ser exatamente 6.")
            return
        
        for n in sorteados:
            if n < 1 or n > 60:
                print("Os números sorteados devem estar entre 1 e 60.")
                return
    except ValueError:
        print("Por favor, insira apenas números separados por vírgula.")
        return
    
    for jogo in jogos:
        id_jogo, numeros = jogo
        numeros = list(map(int, numeros.split()))
        acertos = len(set(numeros) & set(sorteados))
        
        if acertos == 6:
            print(f"Jogo {id_jogo}: {numeros} - Acertou a SENA")
        elif acertos == 5:
            print(f"Jogo {id_jogo}: {numeros} - Acertou a QUINA!")
        elif acertos == 4:
            print(f"Jogo {id_jogo}: {numeros} - Acertou a QUADRA")
        else:
            print(f"Jogo {id_jogo}: {numeros} - Acertou {acertos} números.")

# Função principal do menu do sistema

def menu():
    criar_tabela()
    while True:
        print("\n==== Mega Sena ====")
        print("1. Cadastrar novo jogo")
        print("2. Verificar jogos")
        print("3. Deletar jogo")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_jogo()
        elif opcao == "2":
            verificar_jogos()
        elif opcao == "3":
            deletar_jogo()
        elif opcao == "4":
            print("Encerrando o programa. Boa sorte!")
            break
        else:
            print("Opção inválida! Tente novamente.")

menu()