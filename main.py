import pandas as pd
import random
from collections import OrderedDict
import pickle
import numpy as np
import operator
import random
import pickle
from generate_data import *
from generate_marginal_table import *


num_attribute = 600
num_marginal_tables = 75
size_marginal_tables = 8
epsilon = 10
num_generate_data = 1000



process = 'generate_data' # 'generate_data','generate_marginal_table'


if __name__ == '__main__':
    if process == 'generate_marginal_table':
        raw_data = pd.read_csv('data/dataset', header=None)
        attrs_list = generate_attribute_list(num_attribute,size_marginal_tables,num_marginal_tables) # need consistency
        marginal_list = buil_marginal_table(attrs_list,raw_data,epsilon,is_noise=False)
        with open('data/marginal_table_no_noise.pickle', 'wb') as f:
            pickle.dump(marginal_list, f)

    elif process == 'generate_data':
        filename  = 'data/marginal_table_10_laplace.pickle'
        data = load_marginal_table(filename)
        all_marginal_attrs  = []
        for i in range(len(data)):
            all_marginal_attrs.append(data[i]['attrs'])
        sorted_list = sort_list(all_marginal_attrs) # sort the list

        all_record = []
        for j in range(num_generate_data):
            record = generate_data(sorted_list,data,num_attribute)
            all_record.append(record)
        result = pd.DataFrame(all_record, columns=range(num_attribute))
        result = result.astype(int)

        result.to_csv('data/result_10_laplace.csv')
