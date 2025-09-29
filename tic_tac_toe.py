import pandas as pd
from sklearn import neighbors
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier as DTC

import numpy as np


jogadas_k_nn = []

def k_NN(X, y, teste_X, teste_y, jogos_df):
    clf = neighbors.KNeighborsClassifier(n_neighbors=14)
    clf.fit(X, y) 
    print(f'k = 14 Acurácia = {clf.score(teste_X, teste_y):.4f}') 
    return clf.predict(jogos_df) 

    
def MLP(X,y,teste_X,teste_y,jogos):
    clf = MLPClassifier(hidden_layer_sizes=(50,), activation='relu', solver='sgd', max_iter=10000, learning_rate_init=0.01)
    clf.fit(X, y.ravel())
    predicaos = clf.predict(jogos)
    print(f'Acuracia da MLP = {accuracy_score(teste_y,clf.predict(teste_X))}')
    return predicaos


def arv_decisao(X,y,teste_X,teste_y,jogos):
    modelo = DTC(random_state=42
                ,criterion='log_loss'
                ,min_samples_split=3
                ,ccp_alpha=0.005        # default 0.0 Valores na documentação 0.005 0.01 0.015 0.02 0.025 0.03 0.035
                )
    modelo.fit(X, y)
    teste_pred_y = modelo.predict(teste_X)
    acuracia = accuracy_score(teste_y, teste_pred_y)
    jogos_pred_y = modelo.predict(jogos)
    print(f'Acuracia da Arvore = {acuracia}')
    return jogos_pred_y


def print_mat(mat):
    for l in range(len(mat)):
        str = ''
        for c in range(len(mat)):

           str+=f'{mat[l][c]} '
        print(str)

def main():
    tab = [[0,0,0],[0,0,0],[0,0,0]]
    data = pd.read_csv('amostras_.csv',sep=';')
    X = data.drop(columns=['classe'])
    y = data['classe'].values
    treino_X, teste_X, treino_y, teste_y = tts(X, y, random_state=42,test_size=0.1, stratify=y)
    print(np.stack(np.unique(teste_y, return_counts=True), axis=1))

    while 1:
        
        print_mat(tab)
        break

    jogo = [[0, 1, -1,
             1, -1, -1,
             -1, 1, 1]]
    jogos_df = pd.DataFrame(jogo, columns=X.columns)


    pred_k_nn = k_NN(treino_X,treino_y,teste_X,teste_y,jogos_df)
    print(pred_k_nn)
    pred_mlp = MLP(treino_X,treino_y,teste_X,teste_y,jogos_df)
    print(pred_mlp)
    pred_arv_dec = arv_decisao(treino_X,treino_y,teste_X,teste_y,jogos_df)
    print(pred_arv_dec)

    



if __name__ == '__main__':
    main()