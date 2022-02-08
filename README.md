# K-Medoids-Imputation
The purpose of this project is to impute incomplete datasets with the Partitioning Around Medoids(K-Medoids) algorithm.

Algorithm

Step 1—It splits the dataset X into two observed X_obs and incomplete X_mis subsets.
Step 2—It randomly selects k record from X_obs as initial medoids and put into dataset O_med.
Step3—To cluster the X_obs based on the medoids we choose in step2: For every record in X_obs, we compute its Euclidean distance between it and every medoids, and associate the record to closest medoids.
Step4—It compute the total cost of the clustering. The cost is the summation of the Euclidean distance between every record and its medoid.
Cost =∑_(i=1)^k▒∑_(c∈Ci)▒〖(c-ci)〗
In which Ci stands for the cluster set, ci stands for the medoid of the cluster set, and c stands for the record
Step5—It randomly choose a new set of medoids from each cluster and compute the cost. If the new cost is smaller than the old one, we replace the present medoids with the new medoids.
Step6—It repeat step3-5 until the cost stop become smaller, which means we find the best set of medoids.

Code

There are 3 parts in this project. Kmedoids, Imputation, and Main. 

Kmedoids.py :
It is based on numpy and contains the K-Medoids algorithm. Kmedoids.py has 5 functions. 
KMedoids is the main function. It requires 3 inputs: cluster number, X_obs dataset, and times. It return 2 dataset: ‘centers’, in which contains the index of medoids; and ‘result_cluster’, in which contains the cluster information for every record in X_obs.
    An example of ‘centers’(k =3 ): [23 32 45]
An example of ‘result_cluster’(k= 3, datasize = 10):[0 0 2 0 1 2 2 1 0 2]	
Initialize_centers is the function for step 2 of the algorithm, it requires a number of clustes k,and uses global to get the size of X_obs . It returns a list contains randomly selected indexes of medoids. 
Clus_process is the function for step 3. It requires 2 inputs: a ‘centers ’  from Initialize_centers or chose_centers; and X_obs dataset. And it returns ‘result_cluster’
Count_E is the function to calculate the cost. It requires 3 inputs: ‘centers’, X_obs dataset and ‘result_cluster’. And it return the cost.
Choose_centers is the function for step 5. It requires 2 inputs: ’result_cluster’ and the number of the clusters. And it returns a new sets of ‘centers’.

Imputation.py:

This part is based on numpy and pandas.
It does 2 things: imputes the datasets and calculate the NRMS of the result.
It has 2 part. A main function Imputation to do the imputation. And a toolbox tools, in which contains several functions to help the imputation.

Imputation is the main function in Imputation.py. 
It requires 5 inputs: 
  the number of clusters, 
  names of the features, 
  file path of the incomplete dataset, 
  file path of the original dataset 
loop times.
And it return the NRMS result and the imputed datasets.
Tools:
Loaddata is to read datasets from excel and trans them into pandas dataframe.
Centers2medoids is to pick the medoid from X_obs dataset based on their index in ‘centers’.
Cluster is to cluster the missing data, in order to fill them later. 
Imputedatamis is to fill the missing data.


Main.py

Main needs the operator fill 3 parameters and 3 paths.
K is the number of the clusters.
Names is the names of the features.
Times is not the whole loop times. It is the loop times that the algorithm can not find smaller cost.
Original_path is the path of the original datasets.
Incomplete_path is the path of the folder of the incomplete datasets.
Imputed_path is the path of the folder for the imputed datasets

And there are 2 functions in Main.py.
main go through the folder of incomplete datasets, do the imputation and create a new csv file for every file. It also put the NRMS result in another csv file.
Checkdata is to check if there are complete data in the datasets. Because if all the records have missing data, my algorithm can not work.








