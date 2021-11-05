import numpy as np
from copy import deepcopy
import random
from math import floor
import os

# data = []
# for i in range(300):

#     data.append(i)

# print(len(data))

# dir = "D:\\Desktop\\ECE_542\\ECE_542_Course_Project\\kits19\\data"

# case_ids = os.listdir(dir)

def split(case_ids):
    
    random.seed(42)
    case_ids_copy = deepcopy(case_ids)
    random.shuffle(case_ids_copy)
    num_cases = len(case_ids)

    num_train_val_cases = floor(num_cases*0.7)
    num_test_cases = num_cases - num_train_val_cases

    num_train = floor(num_train_val_cases * 0.8)
    num_val = num_train_val_cases - num_train
    
    train_val_cases = deepcopy(case_ids_copy[:num_train_val_cases])
    test_cases = deepcopy(case_ids_copy[num_train_val_cases:])

    # random.shuffle(train_val_cases)

    train_cases = train_val_cases[:num_train]
    val_cases = train_val_cases[num_train:]

    # print("test", test)
    # print("train", train)
    # print("val", val)

    return {'train':train_cases, 'val':val_cases, 'test':test_cases}

    