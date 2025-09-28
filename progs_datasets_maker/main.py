import random

# precisa conectar o classificador, exemplo predict(tabuleiro_$) que retorna a classe prevista

# Representação do tabuleiro
tabuleiro_ = [[" " for _ in range(3)] for _ in range(3)]

# Contadores de acertos/erros
acertos_ = 0
erros_ = 0
jogadas_ = 0

def exibir_tabuleiro_(tabuleiro_):
    for linha_ in tabuleiro_:
        print("|".join(linha_))
        print("-" * 5)

def verificar_estado_real_(tabuleiro_):
    # Verifica se há vencedor ou empate
    linhas_ = tabuleiro_ + [list(col) for col in zip(*tabuleiro_)]
    diagonais_ = [
        [tabuleiro_[i][i] for i in range(3)],
        [tabuleiro_[i][2 - i] for i in range(3)]
    ]
    for linha_ in linhas_ + diagonais_:
        if linha_[0] != " " and linha_.count(linha_[0]) == 3:
            return "Fim de Jogo"
    if all(c != " " for linha_ in tabuleiro_ for c in linha_):
        return "Fim de Jogo"
    return "Tem jogo"

def jogada_humano_(tabuleiro_):
    while True:
        try:
            linha_, col_ = map(int, input("Digite linha e coluna (0-2): ").split())
            if tabuleiro_[linha_][col_] == " ":
                tabuleiro_[linha_][col_] = "X"
                break
            else:
                print("Posição ocupada!")
        except:
            print("Entrada inválida!")

def jogada_maquina_(tabuleiro_):
    while True:
        l_, c_ = random.randint(0,2), random.randint(0,2)
        if tabuleiro_[l_][c_] == " ":
            tabuleiro_[l_][c_] = "O"
            break

while True:
    exibir_tabuleiro_(tabuleiro_)

    # Jogada do humano
    jogada_humano_(tabuleiro_)
    estado_real_ = verificar_estado_real_(tabuleiro_)
    # IA prediz
    pred_ = "Tem jogo"  # modelo_$.predict(tabuleiro_$) -> PRECISA CONECTAR O CLASSIFICADOR AQUI
    print(f"[IA] Predição: {pred_} | Estado real: {estado_real_}")

    jogadas_ += 1
    if pred_ == estado_real_:
        acertos_ += 1
    else:
        erros_ += 1

    print(f"Acurácia até agora: {acertos_}/{jogadas_}")
    if estado_real_ == "Fim de Jogo":
        break

    # Jogada da máquina
    jogada_maquina_(tabuleiro_)
    estado_real_ = verificar_estado_real_(tabuleiro_)
    pred_ = "Tem jogo"  # modelo_$.predict(tabuleiro_$)
    print(f"[IA] Predição: {pred_} | Estado real: {estado_real_}")

    jogadas_ += 1
    if pred_ == estado_real_:
        acertos_ += 1
    else:
        erros_ += 1

    print(f"Acurácia até agora: {acertos_}/{jogadas_}")
    if estado_real_ == "Fim de Jogo":
        break
