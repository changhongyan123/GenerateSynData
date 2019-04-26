import pandas as pd
import operator
import numpy as np
import random
import pickle

def list_diff(listA,listB):
    # output the differnce of two set
    retB = list(set(listA).intersection(set(listB))) #  common attribute
    retD = list(set(listB).difference(set(listA))) # how much difference
    return len(listA) - len(retD),retB

def get_max_value(all_view,index,all_index):
    # Use for sort the table, get the maximal related one
    # Input
    # all_view: all the marginal tables
    # index: target table
    # all_index: already sorted tables
    # Output
    # index: most related marginal table index

    all_diff = np.zeros((len(all_view)))    # init all the number of common attributes
    index_list = list(range(len(all_view))) # init how many attribute set in the data
    for i in range(len(all_view)):
        if i != index and i not in all_index: # not selected and not the index
            a,b= list_diff(all_view[index],all_view[i]) # get the difference
            all_diff[i] = a # update the difference value
    if sum(all_diff) == 0: #if no set contain a common attribute
        random_index = random.choice([item for item in index_list if item not in all_index])
        return random_index
    index, value = max(enumerate(all_diff), key=operator.itemgetter(1))
    return index


def sort_list(all_view):
    # Sort the marginal table
    # Input
    # all_view: all the marginal tables
    # Output
    # all_index: sorted marginal tables index
    index = random.choice(list(range(len(all_view))))
    all_index = [index]
    for i in range(len(all_view)-1):
        index = get_max_value(all_view,index,all_index)
        all_index.append(index)
    return all_index


def load_marginal_table(filename):
    # load pre-generated marginal tables
    # Input: filename
    # Output: marginal table list
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data


def generate_data(sorted_list,data,num_attrs):
    # Generate data
    # Input:
    # sorted_list: sorted index table for marginal tables
    # data: marginal tables
    # num_attrs: attribute numbers
    record = np.ones(num_attrs) * 1000
    assigned_attrs = []

    for i in range(len(sorted_list)):
        if len(list(set(assigned_attrs))) < num_attrs:
            index = sorted_list[i]
            marginal_data = data[index]['marginal_data']
            attrs = data[index]['attrs']
            record = np.copy(get_assignment(marginal_data,attrs,assigned_attrs,record))
            assigned_attrs = assigned_attrs+attrs
        else:
            break
    return record

def get_assignment(margianl_data,attrs,assigned_attrs,record):
    # Ouput the assignment given a marginal
    # Input:
    # margianl_data: one marginal table
    # attrs: list of attribute of this marginal table
    # assigned_attrs: the attributes has already assigned
    # record: the generated record
    # Output:
    # record: generate data
    for attr in attrs:
        if attr in assigned_attrs:
            margianl_data = margianl_data[margianl_data[attr] == record[attr]]
    if margianl_data['counts'].sum() != 0:
        selected_assignment = margianl_data.sample(axis = 0,weights = margianl_data['counts'])
        attrs = selected_assignment.columns[:-1].values
        for i in range(attrs.shape[0]):
            record[attrs[i]]  = selected_assignment[attrs[i]].values[0]
    return record

# if __name__ == '__main__':
#     filename  = '../data/marginal_table_no_noise.pickle'
#
#     num_record = 100
#     num_attribute = 600
#     data = load_marginal_table(filename)
#     all_marginal_attrs  = []
#     for i in range(len(data)):
#         all_marginal_attrs.append(data[i]['attrs'])
#     sorted_list = sort_list(all_marginal_attrs) # sort the list
#
#     all_record = []
#     for j in range(num_record):
#         record = generate_data(sorted_list,data,num_attribute)
#         all_record.append(record)
#     result = pd.DataFrame(all_record, columns=range(num_attribute))
#     result = result.astype(int)
#
#     result.to_csv('../data/result.csv')
