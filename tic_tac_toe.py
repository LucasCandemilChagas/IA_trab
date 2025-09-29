import pandas as pd
from sklearn.model_selection import train_test_split as tts
from sklearn.neural_network import MLPClassifier
import random
import numpy as np
import os
from sklearn.metrics import accuracy_score

jogadas_k_nn = []

# Representação do tabuleiro
tabuleiro_ = [[0 for _ in range(3)] for _ in range(3)]
tabuleiro_disp = [[' ' for _ in range(3)] for _ in range(3)]

# Contadores de acertos/erros
acertos_ = 0
erros_ = 0
jogadas_ = 0
def limpar_console():
    os.system('cls' if os.name == 'nt' else 'clear')
def exibir_tabuleiro_():
    global tabuleiro_disp
    print('Algoritmo MLP sendo usado!! ')
    for linha_ in tabuleiro_disp:
        print("|".join(linha_))
        print("-" * 5)


def tabuleiro_para_df(board_2d, cols):
    flat = np.array(board_2d, dtype=int).ravel().reshape(1, -1)
    return pd.DataFrame(flat, columns=cols)

def verificar_estado_real_(tabuleiro_):
    # Verifica se há vencedor ou empate
    linhas_ = tabuleiro_ + [list(col) for col in zip(*tabuleiro_)]
    diagonais_ = [
        [tabuleiro_[i][i] for i in range(3)],
        [tabuleiro_[i][2 - i] for i in range(3)]
    ]
    todas_linhas = linhas_ + diagonais_

    # 1) Verifica fim de jogo (alguém venceu ou empate)
    for linha_ in todas_linhas:
        if linha_[0] != 0 and linha_.count(linha_[0]) == 3:
            return "Fim_de_jogo"

    if all(c != 0 for linha_ in tabuleiro_ for c in linha_):
        return "Fim_de_jogo"

    # 2) Verifica possibilidade de fim de jogo
    for linha_ in todas_linhas:
        # Ex.: [1, 1, 0] ou [-1, -1, 0]
        if (linha_.count(1) == 2 and linha_.count(0) == 1) or \
           (linha_.count(-1) == 2 and linha_.count(0) == 1):
            return "Possibilidade_de_fim_de_jogo"

    # 3) Caso contrário, ainda está em jogo
    return "Em_jogo"


def jogada_humano_(tabuleiro_):
    global tabuleiro_disp
    while True:
        try:
            linha_, col_ = map(int, input("Digite linha e coluna (0-2): ").split('-'))
            if tabuleiro_[linha_][col_] == 0:
                tabuleiro_[linha_][col_] = 1
                tabuleiro_disp[linha_][col_] = 'X'
                break
            else:
                print("Posição ocupada!")
        except:
            print("Entrada inválida!")

def jogada_maquina_(tabuleiro_):
    global tabuleiro_disp
    while True:
        l_, c_ = random.randint(0,2), random.randint(0,2)
        if tabuleiro_[l_][c_] == 0:
            tabuleiro_[l_][c_] = -1
            tabuleiro_disp[l_][c_] = 'O'
            break

    
def MLP(X,y):
    clf = MLPClassifier(hidden_layer_sizes=(50,), activation='relu', solver='sgd', max_iter=10000, learning_rate_init=0.01,momentum=0.5)
    clf.fit(X, y.ravel())
    return clf

def print_mat(mat):
    for l in range(len(mat)):
        str = ''
        for c in range(len(mat)):

           str+=f'{mat[l][c]} '
        print(str)

def main():
    global jogadas_, erros_, acertos_
    data = pd.read_csv('amostras_.csv',sep=';')
    X = data.drop(columns=['classe'])
    feature_cols = list(X.columns)
    y = data['classe'].values
    treino_X, _, treino_y, _ = tts(X, y, random_state=42,test_size=0.2, stratify=y)
    mlp = MLP(treino_X,treino_y)
    estado_real_ = None
    pred_ = None
    estados = []
    preds = []
    acertos_ = 0
    erros_ = 0
    while True:
        limpar_console()

        exibir_tabuleiro_() 
        if pred_ is None and estado_real_ is None:
            estado_real_ = verificar_estado_real_(tabuleiro_)
            tab = tabuleiro_para_df(tabuleiro_, feature_cols)
            pred_ = mlp.predict(tab)
            estados.append(estado_real_)
            preds.append(pred_)
            if pred_ == estado_real_:
                acertos_ += 1
            else:
                erros_ += 1
        print(f'Acertos: {acertos_}  Erros: {erros_}')
        print(f"Acurácia até agora: {accuracy_score(estados,preds)}")
        print(f"[IA] Predição: {pred_} | Estado real: {estado_real_}")

        # Jogada do humano
        jogada_humano_(tabuleiro_)
        estado_real_ = verificar_estado_real_(tabuleiro_)

        if estado_real_ == "Fim_de_jogo":
            limpar_console()
            exibir_tabuleiro_() 

            tab = tabuleiro_para_df(tabuleiro_, feature_cols)
            pred_ = mlp.predict(tab)
            estados.append(estado_real_)
            preds.append(pred_)
            if pred_ == estado_real_:
                acertos_ += 1
            else:
                erros_ += 1
            print(f'Acertos: {acertos_}  Erros: {erros_}')
            print(f"Acurácia final: {accuracy_score(estados,preds)}")
            print(f"[IA] Predição final: {pred_} | Estado real: {estado_real_}")
            print('VOCE VENCEU!!')
            break

        # Jogada da máquina
        jogada_maquina_(tabuleiro_)
        estado_real_ = verificar_estado_real_(tabuleiro_)
        tab = tabuleiro_para_df(tabuleiro_, feature_cols)
        pred_ = mlp.predict(tab)
        estados.append(estado_real_)
        preds.append(pred_)
        if pred_ == estado_real_:
            acertos_ += 1
        else:
            erros_ += 1

        if estado_real_ == "Fim_de_jogo":
            limpar_console()
            exibir_tabuleiro_() 
            print(f'Acertos: {acertos_}  Erros: {erros_}')
            print(f"Acurácia final: {accuracy_score(estados,preds)}")
            print(f"[IA] Predição final: {pred_} | Estado real: {estado_real_}")
            print('VOCE PERDEU!!')
            break

if __name__ == '__main__':
    main()