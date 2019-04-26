import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.optimize import linear_sum_assignment



def statistic_error(clean_data,target_data):

    c_mean =  clean_data.mean().values
    s_mean = target_data.mean().values
    if s_mean.shape[0] > c_mean.shape[0]:
        s_mean = s_mean[1:]
    mean_diff = c_mean - s_mean
    return np.sum(mean_diff*mean_diff)

def get_kmeans_center(dataset,file_name):
    if dataset.shape[1] > 600:
        dataset = dataset.drop(dataset.columns[0],axis=1)
    kmeans = KMeans(n_clusters=100, random_state=0).fit(dataset)
    center = kmeans.cluster_centers_
    np.save(file_name, center)

def save_dataset_center(dataset_name,center_name,data=None,is_load=True):
    if is_load == True:
        filename = 'data/' + dataset_name
        data = pd.read_csv(filename,header=None)
    else:
        data = data
    c_file_name = 'data/'+ center_name +'.npy'
    get_kmeans_center(data,c_file_name)




if __name__ == '__main__':
    clean_cen = np.load('data/clean_data.npy')
    clean_data = pd.read_csv('data/dataset',header=None)
    file_list = ['data/result_3_laplace.csv','data/result_10_laplace.csv','data/result_no_noise.csv','data/random_clean_data.csv']
    file_name_list = ['laplace 3','laplace 10','no noise','random selected']


    for i in range(len(file_list)):
        file = file_list[i]
        file_name = file_name_list[i]
        data = pd.read_csv(file)
        data = data.drop(['Unnamed: 0'],axis=1)

        kmeans = KMeans(n_clusters=100, random_state=0).fit(data)
        data_cen = kmeans.cluster_centers_
        cost = np.zeros((100,100))
        mean_score = statistic_error(clean_data,data)
        for i in range(100):
            cost[i] = np.sum(( data_cen[i]-clean_cen)*( data_cen[i]-clean_cen),axis=1)
            row_ind, col_ind = linear_sum_assignment(cost)
            k_score = cost[row_ind, col_ind].sum()
        print(file_name)
        print('mean error: %.6f' %mean_score)
        print('k means error: %.6f' %k_score)
