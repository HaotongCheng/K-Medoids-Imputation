import numpy as np
import random


def initialize_centers(n_clusters):
    """initianlize and randomly choose cluster centors"""
    global n_data
    centers = []  # example of centers of medoids：[101,205,5,3,7]
    i = 0
    while i < n_clusters:
        try:
            temp = random.randint(0, n_data - 1)
        except:
            print('lengh of data_obs',n_data)
        if temp not in centers:
            centers.append(temp)
            i = i + 1
        else:
            pass
    return centers


def clus_process(centers, data):
    """clustering based on cluster centors"""
    result_clusters = []
    centers = np.array(centers)

    for i in range(0, len(data)):
        uni_temp = []  #  storage distance data temporary
        for j in centers:
            temp = np.sqrt(np.sum(np.square(data[i] - data[j])))
            uni_temp.append(temp)
        c_min = min(uni_temp)  # Minimum distance
        result_clusters.append(uni_temp.index(c_min))  # location of minimun distance is the cluster
    return result_clusters


def chose_centers(result_clusters, n_clusters):
    centers = []
    for i in range(0, n_clusters):  # for every cluster
        temp = []  # Record the position of each cluster sample in data
        for j in range(0, len(result_clusters)):  # go through every sasmple
            if result_clusters[j] == i:  # Find samples of cluster i
                temp.append(j)
        try:
            c_temp = random.sample(temp, 1)  # Randomly select a value in the sample as the new cluster center
        except:
            print("sample bug")
            print(temp)
        centers.append(c_temp[0])

    return centers


def count_E(centers, data, result_clusters):
    """compute cost"""
    E = 0
    for i in range(0, len(centers)):
        for j in range(0, len(data)):
            if result_clusters[j] == i:
                temp = np.sqrt(np.sum(np.square(data[j] - data[centers[i]])))
                E += temp
    return E


def KMedoids(n_clusters, data, max_iter):
    """initialized"""
    global n_data
    n_data = len(data)
    centers = initialize_centers(n_clusters)
    """clustering"""
    result_clusters = clus_process(centers, data)
    """reclustering and compare"""
    count = 0  # counter
    E = count_E(centers, data, result_clusters)

    while count <= max_iter:
        centers_new = chose_centers(result_clusters, n_clusters)  # select new medoids
        result_clusters_new = clus_process(centers, data)  #  new cluster result
        """compute cost E"""
        E_new = count_E(centers_new, data, result_clusters_new)
        """If the value function becomes smaller, update the cluster center and cluster result"""
        if E_new < E:
            centers = centers_new
            result_clusters = result_clusters_new
            E = E_new
            print("cost:%s" % E)
            print("centers:%s" % centers)
            count = 0
        """counter"""
        count = count + 1
        if count % 10 == 0 and count != 0:
            print(count)

    return centers, result_clusters






