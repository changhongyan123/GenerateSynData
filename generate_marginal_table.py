import csv
import pandas as pd
import random
from collections import OrderedDict
import pickle
import numpy as np




def generate_attribute_list(num_attrs,marginal_size,num_margianl_tables):
    marginal_attrs = []
    all_attributes = list(range(num_attrs))
    while len(all_attributes) > 0:
        attr = random.sample(all_attributes, marginal_size)
        all_attributes = [x for x in all_attributes if x not in attr]
        marginal_attrs.append(attr)
    return marginal_attrs


def buil_marginal_table(marginal_attrs,data,epsilion,is_noise = False):
    marginal_list = []
    for i in range(len(marginal_attrs)):
        attrs = marginal_attrs[i]
        marginal_table = {}
        marginal_data = data[attrs].groupby(attrs)[attrs[1]].count().reset_index(name='counts')
        if is_noise == True:
            noise = np.random.laplace(0, len(marginal_attrs)/epsilion, marginal_data['counts'].shape[0])
            marginal_data['counts'] =   marginal_data['counts'] + noise
            marginal_data['counts'] = marginal_data['counts'] - marginal_data['counts'].min()
        marginal_table['attrs'] = attrs
        marginal_table['marginal_data'] = marginal_data
        marginal_list.append(marginal_table)
    return marginal_list



#
# if __name__ == '__main__':
#     num_margianl = 300
#     marginal_size = 8
#     num_attrs = 600
#     epsilon = 3
#
#
#     raw_data = pd.read_csv('../data/dataset', header=None)
#     attrs_list = generate_attribute_list(num_attrs,marginal_size,num_margianl) # need consistency
#     marginal_list = buil_marginal_table(attrs_list,raw_data,epsilon)
#     with open('../data/marginal_table_no_noise.pickle', 'wb') as f:
#         pickle.dump(marginal_list, f)
