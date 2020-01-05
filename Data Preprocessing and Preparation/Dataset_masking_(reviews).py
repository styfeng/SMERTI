# -*- coding: utf-8 -*-
import io, json, os, collections, pprint, time
import re
from string import punctuation
from random import sample
import math
import unicodedata


def mask_all(path, total):
    mask_list = []
    f = io.open(path, encoding = 'utf-8')
    counter = 0
    print("Currently reading lines from file ...")
    for l in f:
        if 0 <= counter <= int(round(total / 3)):
            masked_review = mask_text(l, 0.15)
        elif int(round(total / 3)) < counter <= int(round((total * 2) / 3)):
            masked_review = mask_text(l, 0.30)
        else:
            masked_review = mask_text(l, 0.45)
        #For transformer:
        mask_list.append(masked_review + '\n')
        #For RNN:
        #mask_list.append(masked_review + '\t' + l) 
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


path1 = os.path.expanduser('Yelp_Dataset/transformer_data/train_reviews_positive.txt')
path2 = os.path.expanduser('Yelp_Dataset/transformer_data/train_reviews_negative.txt')
path3 = os.path.expanduser('Yelp_Dataset/transformer_data/train_reviews_neutral.txt')
    
path4 = os.path.expanduser('Yelp_Dataset/transformer_data/valid_reviews_positive.txt')
path5 = os.path.expanduser('Yelp_Dataset/transformer_data/valid_reviews_negative.txt')
path6 = os.path.expanduser('Yelp_Dataset/transformer_data/valid_reviews_neutral.txt')
    
path7 = os.path.expanduser('Yelp_Dataset/transformer_data/test_reviews_positive.txt')
path8 = os.path.expanduser('Yelp_Dataset/transformer_data/test_reviews_negative.txt')
path9 = os.path.expanduser('Yelp_Dataset/transformer_data/test_reviews_neutral.txt')

path10 = os.path.expanduser('Yelp_Dataset/transformer_data/final_train_reviews.txt')
path11 = os.path.expanduser('Yelp_Dataset/transformer_data/final_valid_reviews.txt')
path12 = os.path.expanduser('Yelp_Dataset/transformer_data/final_test_reviews.txt')


path13 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_train_reviews_positive.txt')
path14 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_train_reviews_negative.txt')
path15 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_train_reviews_neutral.txt')
    
path16 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_valid_reviews_positive.txt')
path17 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_valid_reviews_negative.txt')
path18 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_valid_reviews_neutral.txt')
    
path19 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_test_reviews_positive.txt')
path20 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_test_reviews_negative.txt')
path21 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_test_reviews_neutral.txt')

path22 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_final_train_reviews.txt')
path23 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_final_valid_reviews.txt')
path24 = os.path.expanduser('Yelp_Dataset/transformer_data/mask_final_test_reviews.txt')


train_positive = 30000
train_negative = 30000
train_neutral = 15000

valid_positive = 5000
valid_negative = 5000
valid_neutral = 2500

test_positive = 5000
test_negative = 5000
test_neutral = 2500

mask_train_positive = mask_all(path1, train_positive)
mask_train_negative = mask_all(path2, train_negative)
mask_train_neutral = mask_all(path3, train_neutral)

mask_valid_positive = mask_all(path4, valid_positive)
mask_valid_negative = mask_all(path5, valid_negative)
mask_valid_neutral = mask_all(path6, valid_neutral)

mask_test_positive = mask_all(path7, test_positive)
mask_test_negative = mask_all(path8, test_negative)
mask_test_neutral = mask_all(path9, test_neutral)

final_mask_train_reviews = mask_train_positive + mask_train_negative + mask_train_neutral
final_mask_valid_reviews = mask_valid_positive + mask_valid_negative + mask_valid_neutral
final_mask_test_reviews = mask_test_positive + mask_test_negative + mask_test_neutral


#write_file(mask_train_positive, path13)
#write_file(mask_train_negative, path14)
#write_file(mask_train_neutral, path15)

#write_file(mask_valid_positive, path16)
#write_file(mask_valid_negative, path17)
#write_file(mask_valid_neutral, path18)

#write_file(mask_test_positive, path19)
#write_file(mask_test_negative, path20)
#write_file(mask_test_neutral, path21)

#write_file(final_mask_train_reviews, path22)
#write_file(final_mask_valid_reviews, path23)
#write_file(final_mask_test_reviews, path24)