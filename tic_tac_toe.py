import pandas as pd
from sklearn import neighbors
from sklearn.model_selection import train_test_split as tts

jogadas_k_nn = []

def k_NN(X,y,teste_X,teste_y,jogos):
    clf = neighbors.KNeighborsClassifier(n_neighbors=14)
    clf.fit(X.values, y)
    predicao = clf.predict(jogos)
    print(f'k = 14 Acuracia = {clf.score(teste_X.values,teste_y)}')
    return predicao

    
def MLP():
    pass

def arv_decisao():
    pass



def main():

    data = pd.read_csv('amostras_.csv',sep=';')
    X = data.drop(columns=['classe'])
    y = data['classe'].values
    treino_X, teste_X, treino_y, teste_y = tts(X, y, random_state=42,test_size=0.1, stratify=y)
    
    pred = k_NN(treino_X,treino_y,teste_X,teste_y,[[1,0,-1,
                                                    0,1,-1,
                                                    0,0,1]])
    print(pred)


    



if __name__ == '__main__':
    main()