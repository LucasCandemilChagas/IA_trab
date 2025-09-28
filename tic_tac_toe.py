import pandas as pd
from sklearn import neighbors
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier


jogadas_k_nn = []

def k_NN(X,y,teste_X,teste_y,jogos):
    clf = neighbors.KNeighborsClassifier(n_neighbors=14)
    clf.fit(X.values, y)
    predicao = clf.predict(jogos)
    print(f'k = 14 Acuracia = {clf.score(teste_X.values,teste_y)}')
    return predicao

    
def MLP(X,y,teste_X,teste_y,jogos):
    clf = MLPClassifier(hidden_layer_sizes=(50,), activation='relu', solver='sgd', max_iter=1000, learning_rate_init=0.01)
    clf.fit(X, y.ravel())
    predicaos = clf.predict(jogos)
    print(f'Acuracia da MLP = {accuracy_score(teste_y,clf.predict(teste_X))}')
    return predicaos


def arv_decisao():
    pass

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
    treino_X, teste_X, treino_y, teste_y = tts(X, y, random_state=42,test_size=0.2, stratify=y)

    while 1:
        
        print_mat(tab)
        break

    jogo = [[0,1,-1,
             1,-1,-1,
             -1,1,1,]]


    pred = k_NN(treino_X,treino_y,teste_X,teste_y,jogo)
    print(pred)
    preds = MLP(treino_X,treino_y,teste_X,teste_y,jogo)
    print(preds)
   

    



if __name__ == '__main__':
    main()