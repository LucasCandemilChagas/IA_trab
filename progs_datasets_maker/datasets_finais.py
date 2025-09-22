from dataset_maker import DataSet_Maker

import glob
import os

def main():
    #DataSet_Maker().exec()
    DataSet_Maker().exec_()
    DataSet_Maker().exec_all()
    #for arquivo in glob.glob("*.txt"):
    #    os.remove(arquivo)

if __name__ == "__main__":
    main()