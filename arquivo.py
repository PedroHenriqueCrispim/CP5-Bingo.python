import random #gerar numeros aleatorios

#função para criar a cartela
def criar_cartela():
    cartela = [[0] * 5 for _ in range(5)]  #inicia uma matriz 5x5 para a cartela
    colunas = [list(range(1, 16)), list(range(16, 31)), list(range(31, 46)), list(range(46, 61)), list(range(61, 76))]  #organiza a cartela de forma q as colunas fiquem do jeito q foi pedido

    for i in range(5):
        for j in range(5):
            coluna = colunas[j]
            numero = random.choice(coluna)  #escolhe os número aleatório da coluna
            coluna.remove(numero)  #remove o número escolhido da coluna pra nao repetir
            cartela[i][j] = numero  #preenche a cartela com o número escolhido

    return cartela

#função para imprimir uma cartela de Bingo em formato de matriz
def imprimir_cartela(cartela):
    for linha in cartela:
        for numero in linha:
            print(str(numero).rjust(2), end=' ')  #formata e imprime os números na cartela
        print()

#função para marcar um número na cartela
def marcar_numero(cartela, numero):
    for i in range(5):
        for j in range(5):
            if cartela[i][j] == numero:
                cartela[i][j] = 'XX'  #marca o número com 'XX' quando é sorteado
                return True
    return False

#função para ver quem ganhou 
def jogador_venceu(cartela):
    #verifica as linhas horizontais e verticais
    for i in range(5):
        if all([cartela[i][j] == 'XX' for j in range(5)]) or all([cartela[j][i] == 'XX' for j in range(5)]):
            return True

    #verifica as diagonais
    if all([cartela[i][i] == 'XX' for i in range(5)]) or all([cartela[i][4 - i] == 'XX' for i in range(5)]):
        return True

    return False

#função para atualizar o arquivo de ranking
def atualizar_ranking(vencedor, arquivo_ranking):
    try:
        with open(arquivo_ranking, 'r') as arquivo:
            ranking = arquivo.readlines()
    except FileNotFoundError:
        ranking = []

    # Encontra o jogador no ranking atual
    jogador_encontrado = False
    for i, linha in enumerate(ranking):
        if ',' in linha:
            elementos = linha.strip().split(',')
            if len(elementos) == 2:
                nome, vitorias = elementos
                if nome == vencedor:
                    ranking[i] = f"{nome}-{int(vitorias) + 1}\n"
                    jogador_encontrado = True
                    break

    # Adiciona o jogador se ele não estiver no ranking
    if not jogador_encontrado:
        ranking.append(f"{vencedor},1\n")

    if ranking:
        # Ordena os jogadores de quem tem mais vitórias para quem tem menos
        ranking.sort(
            key=lambda x: int(x.strip().split(',')[1]) if len(x.strip().split(',')) == 2 else 0,
            reverse=True)
    else:
        # Se o ranking estiver vazio, não há necessidade de ordenação
        ranking = [f"{vencedor},1\n"]

    # Escreve o ranking atualizado de volta no arquivo
    with open(arquivo_ranking, 'w') as arquivo:
        arquivo.writelines(ranking)
        
#função para exibir o ranking
def exibir_ranking(arquivo_ranking):
    try:
        with open(arquivo_ranking, 'r') as arquivo:
            ranking = arquivo.readlines()
        if ranking:
            print("Ranking de Jogadores:")
            print()
            for i, linha in enumerate(ranking, start=1):
                elementos = linha.strip().split(',')
                if len(elementos) == 2:
                    nome, vitorias = elementos
                    print(f"{i}. {nome}: {vitorias} vitórias")
                    print()
        else:
            print("O ranking está vazio.")
    except FileNotFoundError:
        print("O arquivo de ranking ainda não existe.")


#função principal do jogo
def jogar_bingo():
    arquivo_ranking = "ranking.txt"

    print("Bem-vindo ao Jogo de Bingo!")
    
    num_jogadores = int(input("Quantos jogadores participarão (1 a 5)? "))
    if num_jogadores < 1 or num_jogadores > 5:
        print("Número inválido de jogadores. O jogo suporta de 1 a 5 jogadores.")
        return

    nomes_jogadores = []
    for i in range(num_jogadores):
        nome = input(f"Nome do Jogador {i + 1}: ")
        nomes_jogadores.append(nome)

    cartelas = [criar_cartela() for _ in range(num_jogadores)]
    
    print("\nCartelas dos Jogadores:")
    for i, cartela in enumerate(cartelas, start=1):
        print(f"\nCartela do Jogador {i}:")
        imprimir_cartela(cartela)

    numeros_sorteados = []
    
    while True:
        input("Pressione Enter para sortear um número...")
        numero_sorteado = random.randint(1, 75)
        if numero_sorteado not in numeros_sorteados:
            print(f"Número sorteado: {numero_sorteado}")
            numeros_sorteados.append(numero_sorteado)
            
            for i, cartela in enumerate(cartelas, start=1):
                if marcar_numero(cartela, numero_sorteado):
                    print(f"Cartela do Jogador {i} atualizada:")
                    imprimir_cartela(cartela)
                    if jogador_venceu(cartela):
                        vencedor = nomes_jogadores[i-1]
                        print()
                        print(f"Jogador {vencedor} venceu!")
                        print()
                        atualizar_ranking(vencedor, arquivo_ranking) 
                        exibir_ranking(arquivo_ranking) 
                        return

if __name__ == "__main__":
    jogar_bingo()
