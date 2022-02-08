import copy
import numpy as np
import pandas as pd
import KMedoids as KMedoids




class tools:


 def loaddata(file_path, names):
     """
     load data
     """
     dataset = pd.read_excel(file_path, names=names, header=None)
     data_obs = dataset.dropna(axis=0, how='any')
     data_mis = dataset[dataset.isnull().T.any()]
     ##data_mis = dataset.append(data_obs).drop_duplicates(keep=False)
     return data_obs, data_mis, dataset


 def centers2medoids(centers, data):
     medoids = np.array(data[centers[0]])
     temp = np.array([])
     for i in range(1, len(centers)):
         temp = np.array(data[centers[i]])
         medoids = np.vstack([medoids, temp])
     return medoids


 def meanofcluster(k, features, result_clusters, data_obs_np):
     meanofcluster = np.zeros((k, features))
     for j in range(0, k):
         sum = np.zeros((1, 4))
         temp = []
         mean = []
         count = 0
         for i in range(0, len(result_clusters)):
             if result_clusters[i] == j:
                 temp = data_obs_np[i]
                 sum = sum + temp
                 count += 1
         mean = sum.mean(axis=0)/count
         meanofcluster[j] = mean
     return meanofcluster


 def cluster(medoids_DF,data_mis):
     """clustering missing data"""
     result = []
     for i in range(0, len(data_mis)):
         medoids_DF1 = medoids_DF.append(data_mis.iloc[i])
         medoids_DF2 = medoids_DF1.dropna(axis=1, how='any')
         medoids_DF_n = medoids_DF2.to_numpy()
         mis = medoids_DF_n[-1]
         medoids_DF3 = medoids_DF2.drop(medoids_DF2.tail(1).index)
         medoids_DF_np = medoids_DF3.to_numpy()
         # print('medoids_DF',medoids_DF)
         # print('mis', mis)
         uni_temp = []
         for j in range(0, len(medoids_DF3)):
             temp = np.sqrt(np.sum(np.square(mis[0] - medoids_DF_np[j])))
             uni_temp.append(temp)
         c_min = min(uni_temp)
         result.append(uni_temp.index(c_min))
     return result


 def imputedatamis(data_mis, medoids_np, result):
     data_mis_np = data_mis.to_numpy()
     imputed_datamis = copy.deepcopy(data_mis)
     for i in range(0, len(data_mis)):
         temp = pd.DataFrame([data_mis_np[i], medoids_np[result[i]]])
         temp = temp.fillna(method='bfill')
         temp = temp.to_numpy()
         imputed_datamis.iloc[i] = temp[0]
     return imputed_datamis


def Imputation(k, names, file_path0,file_path1,times):

    """to show all the records"""
    np.set_printoptions(threshold=np.inf)
    pd.set_option('display.max_rows', None)

    """load data"""
    data_obs, data_mis, dataset = tools.loaddata(file_path0,names)
    data_obs = data_obs.to_numpy()


    """use Kmedoids to find location of medoids and cluster the data_obs"""
    centers, result_clusters = KMedoids.KMedoids(k, data_obs, times)
    print('centers',centers)
    print('result clusters',result_clusters)

    """pick the medoids based on there location"""
    medoids_np = tools.centers2medoids(centers, data_obs)
    medoids_DF = pd.DataFrame(medoids_np, columns=names)
    y=len(dataset) + 1
    for i in range(0, len(medoids_DF)):
        medoids_DF = medoids_DF.rename({i:y}, axis='index')
        y += 1
    print('medoids_DF',medoids_DF)

    """cluster the missing data and fill them"""
    result = tools.cluster(medoids_DF,data_mis)
    # print('result',result)
    imputedatamis = tools.imputedatamis(data_mis, medoids_np, result)
    # print('datamis',data_mis)
    # print('imputedatamis',imputedatamis)

    """imputaion"""
    for i in range(0, len(data_mis)):
        dataset.iloc[data_mis.iloc[i].name] = imputedatamis.iloc[i]

    """calculate the NRMS"""
    dataset_ori = pd.read_excel(file_path1, names=names,header=None)
    x_est = dataset.to_numpy()
    x_ori = dataset_ori.to_numpy()
    NRMS = np.linalg.norm(x_est-x_ori, ord='fro', keepdims=False)/np.linalg.norm(x_ori, ord='fro', keepdims=False)
    print('NRMS', NRMS)
    print('xestimate-xoriginal', np.linalg.norm(x_est - x_ori, ord='fro', keepdims=False))
    print('xorigianl', np.linalg.norm(x_ori, ord='fro', keepdims=False))
    print('data_mis',len(data_mis))
    return NRMS, dataset


    # print('dataset',dataset,len(dataset))
    # print('dataobs',len(data_obs))
    # print('datamis',len(data_mis))
    # pd.set_option('display.max_rows', None)
    # print('dataset',dataset)
