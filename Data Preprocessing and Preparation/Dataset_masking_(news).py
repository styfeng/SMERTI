# -*- coding: utf-8 -*-
import io, json, os, collections, pprint, time
import re
from string import punctuation
from random import sample
import math


def mask_all(path, total):
    mask_list = []
    f = io.open(path, encoding = 'utf-8')
    counter = 0
    print("Currently reading lines from file ...")
    for l in f:
        if 0 <= counter <= int(round(total / 3)):
            masked_headline = mask_text(l, 0.15)
        elif int(round(total / 3)) < counter <= int(round((total * 2) / 3)):
            masked_headline = mask_text(l, 0.30)
        else:
            masked_headline = mask_text(l, 0.45)
        #For transformer:
        mask_list.append(masked_headline + '\n')
        #For RNN:
        mask_list.append(masked_headline + '\t' + l)   
        counter += 1
    return mask_list


def mask_text(line, value):
    word_list = (line.rstrip()).split()
    num = int(round(len(word_list) * value))
    mask_locs = set(sample(range(len(word_list)), num))
    masked = list(('[mask]' if i in mask_locs and word_list[i] not in punctuation else c for i,c in enumerate(word_list)))
    masked_groups = mask_groupings(masked)
    masked_text = ' '.join(masked_groups)
    return masked_text


def mask_groupings(masked_list):
    masked_group_list = []
    previous_element = ""
    for element in masked_list:
        if element != "[mask]":
            masked_group_list.append(element)
        elif element == "[mask]":
            if element != previous_element:
                masked_group_list.append(element)
        previous_element = element
    return masked_group_list


def write_file(lst, path):
    f = io.open(path, "w", encoding = 'utf-8')
    print("Currently writing lines to file ...")
    f.writelines(lst)
    f.close()
    print("Lines successfully written to file!")


path1 = os.path.expanduser('News_Dataset/transformer_data/train_headlines.txt')
path2 = os.path.expanduser('News_Dataset/transformer_data/val_headlines.txt')
path3 = os.path.expanduser('News_Dataset/transformer_data/test_headlines.txt')
path4 = os.path.expanduser('News_Dataset/transformer_data/masked_train_headlines.txt')
path5 = os.path.expanduser('News_Dataset/transformer_data/masked_val_headlines.txt')
path6 = os.path.expanduser('News_Dataset/transformer_data/masked_test_headlines.txt')

total_headlines_train = 120000
total_headlines_val = 20000
total_headlines_test = 20000

mask_train_list = mask_all(path1, total_headlines_train)
mask_val_list = mask_all(path2, total_headlines_val)
mask_test_list = mask_all(path3, total_headlines_test)

#write_file(mask_train_list, path4)
#write_file(mask_val_list, path5)
#write_file(mask_test_list, path6)