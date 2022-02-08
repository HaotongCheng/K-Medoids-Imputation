import copy
import numpy as np
import pandas as pd
import os
import Imputation as Imputation


def loaddata(file_path, names):
    """
    load data
    """
    dataset = pd.read_excel(file_path, names = names,header=None)
    data_obs = dataset.dropna(axis=0, how='any')
    data_mis = dataset[dataset.isnull().T.any()]
    ##data_mis = dataset.append(data_obs).drop_duplicates(keep=False)
    data_obs = data_obs.to_numpy()
    return data_obs, data_mis, dataset


"""k = number of clusters"""
k = 3

"""names = ['a1','a2','a3','a4','a5','a6','a7','a8','a9','a10',\
         'a11','a12','a13','a14','a15','a16','a17','a18','a19','a20',\
         'a21','a22','a23','a24','a25','a26','a27','a28','a29','a30',\
         'a31','a32','a33','a34','a35','a36','a37','a38','a39','a40',\
         'a41','a42','a43','a44','a45','a46','a47','a48','a49','a50',\
         'a51','a52','a53','a54','a55','a56','a57','a58','a59','a60'] """
names = ['a1','a2','a3','a4']

"""if cannot find smaller cost in n times the loop will end"""
times = 100


Original_path = 'Original Datasets Without Labels\Iris.xlsx'
Incomplete_path = 'Incomplete Datasets Without Labels\Iris'
Imputed_path = 'Imputed Datasets/Iris'
files = os.listdir(Incomplete_path)


"""check if data_obs is empty"""
def checkdata (files,Incomplete_path,names):
    tr = '\\'
    count = 0
    for file in files:
        filename = Incomplete_path + tr + file
        data_obs, data_mis, dataset = loaddata(filename, names)
        count += 1
        print(count)
        if len(data_obs) <= k:
            print(file, 'data_obs', len(data_obs), 'data_mis', len(data_mis), 'dataset', len(dataset))


""" main """
def main(k, names, times, files, Incomplete_path,Original_path,Imputed_path):
    file_nrms = pd.DataFrame([], columns=['name', 'Nrms'])
    tr = '\\'
    for file in files:
        filepath = Incomplete_path + tr + file
        NRMS, dataset = Imputation.Imputation(k, names, filepath, Original_path, times)
        dataset.to_csv(Imputed_path + tr +file + '.csv', header=None)
        file_nrms = file_nrms.append([[file, NRMS]])
        print(file_nrms)
        file_nrms.to_csv('NRMS_result.csv')


checkdata(files,Incomplete_path,names)
main(k, names, times, files, Incomplete_path,Original_path,Imputed_path)









