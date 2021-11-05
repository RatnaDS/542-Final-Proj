import numpy as np
from copy import deepcopy
import random
from math import floor
import os

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

    train_cases = train_val_cases[:num_train]
    val_cases = train_val_cases[num_train:]

    return {'train':train_cases, 'val':val_cases, 'test':test_cases}

    
def retrieve_split_files(splits, data_dir, base_dir):
    
    files = sorted(os.listdir(data_dir))

    filestore = {
        "train": [],
        "val": [],
        "test": []
    }

    for split, case_ids in splits.items():
        for case_id in sorted(case_ids):
            print(case_id)
            files_to_take = [os.path.join(base_dir, file) for file in files if case_id in file]
            filestore[split] += files_to_take
    return filestore


def make_files(save_dir, filename, files):

    writestring = "\n".join(files)

    with open(os.path.join(save_dir, filename), "w") as f:
        f.write(writestring)
