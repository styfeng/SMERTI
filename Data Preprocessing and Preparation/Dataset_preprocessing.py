# -*- coding: utf-8 -*-
import io, json, os, collections, pprint, time
import re
from string import punctuation
import unicodedata
import random


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')


def process_text(s):
    s = unicodeToAscii(s.lower().strip()) 
    s = re.sub('\!+', '!', s)
    s = re.sub('\,+', ',', s)
    s = re.sub('\?+', '?', s)
    s = re.sub('\.+', '.', s)    
    s = re.sub("[^a-zA-Z.!?,'']+", ' ', s)
    for p in punctuation:
        if p not in ["'", "[", "]"]:
            s = s.replace(p, " " + p + " ")       
    s = re.sub(' +', ' ', s)
    s = s.strip()
    return s


def filter_headlines(path, max_length):
    headline_list = []
    f = io.open(path, encoding = 'utf-8')
    counter = 0
    print("Currently reading lines from file ...")
    for l in f:
        if counter % 10000 == 0:
            print("Read in {%d} lines" % counter)
        jline = json.loads(l)
        if len(jline['headline'].split()) <= max_length and jline['headline'] != '' and isEnglish(jline['headline']) \
           and 'http' not in jline['headline'].lower() and 'www' not in jline['headline'].lower():
            clean_line = re.sub('\s+', ' ', jline['headline']).strip()
            clean_line_final = process_text(clean_line)
            headline_list.append(clean_line_final + '\n')
        counter += 1
    return headline_list


def filter_reviews(path, max_length, dataset):
    review_list = []
    positive_list = []
    negative_list = []
    neutral_list = []
    f = io.open(path, encoding = 'utf-8')
    counter = 0
    print("Currently reading lines from file ...")
    
    if dataset.lower() == 'yelp':
        for l in f:
            if counter % 100000 == 0:
                print("Read in {%d} lines" % counter)
            jline = json.loads(l)
            if len(jline['text'].split()) <= max_length and jline['text'] != '' and isEnglish(jline['text']) \
               and 'http' not in jline['text'].lower() and 'www' not in jline['text'].lower():
                clean_line = re.sub('\s+', ' ', jline['text']).strip()
                clean_line_final = process_text(clean_line)
                if jline['stars'] < 3.0:
                    negative_list.append(clean_line_final + '\n')
                elif jline['stars'] == 3.0:
                    neutral_list.append(clean_line_final + '\n')
                else:
                    positive_list.append(clean_line_final + '\n')
                review_list.append(clean_line_final + '\n')
            counter += 1
    
    elif dataset.lower() == 'amazon':
        for l in f:
            if counter % 100000 == 0:
                print("Read in {%d} lines" % counter)
            jline = json.loads(l)
            if len(jline['reviewText'].split()) <= max_length and jline['reviewText'] != '' and isEnglish(jline['reviewText']) and 'http' not in jline['reviewText'].lower() and 'www' not in jline['reviewText'].lower():
                clean_line = re.sub('\s+', ' ', jline['reviewText']).strip()
                clean_line_final = process_text(clean_line)
                if jline['overall'] < 3.0:
                    negative_list.append(clean_line_final + '\n')
                elif jline['overall'] == 3.0:
                    neutral_list.append(clean_line_final + '\n')
                else:
                    positive_list.append(clean_line_final + '\n')
                review_list.append(clean_line_final + '\n')
            counter += 1        
    
    return review_list, positive_list, negative_list, neutral_list


def write_file(lst, path):
    f = io.open(path, "w", encoding = 'utf-8')
    print("Currently writing lines to file ...")
    f.writelines(lst)
    f.close()
    print("Lines successfully written to file!")


    
#For news headlines:

path1 = os.path.expanduser('News_Dataset/News_Category_Dataset_v2.json')
path2 = os.path.expanduser('News_Dataset/train_headlines.txt')
path3 = os.path.expanduser('News_Dataset/val_headlines.txt')
path4 = os.path.expanduser('News_Dataset/test_headlines.txt')

max_length = 20

headline_list = filter_headlines(path1, max_length)
total_headlines = len(headline_list)
print("Total number of headlines: ", total_headlines)

random.shuffle(headline_list)

train_list = headline_list[:120000]
val_list = headline_list[120000:140000]
test_list = headline_list[140000:160000]

#write_file(train_list, path2)
#write_file(val_list, path3)
#write_file(test_list, path4)


#For reviews:

path1 = os.path.expanduser('Yelp_Dataset/review.json')

path2 = os.path.expanduser('Yelp_Dataset/train_reviews_positive.txt')
path3 = os.path.expanduser('Yelp_Dataset/train_reviews_negative.txt')
path4 = os.path.expanduser('Yelp_Dataset/train_reviews_neutral.txt')

path5 = os.path.expanduser('Yelp_Dataset/valid_reviews_positive.txt')
path6 = os.path.expanduser('Yelp_Dataset/valid_reviews_negative.txt')
path7 = os.path.expanduser('Yelp_Dataset/valid_reviews_neutral.txt')

path8 = os.path.expanduser('Yelp_Dataset/test_reviews_positive.txt')
path9 = os.path.expanduser('Yelp_Dataset/test_reviews_negative.txt')
path10 = os.path.expanduser('Yelp_Dataset/test_reviews_neutral.txt')

path11 = os.path.expanduser('Yelp_Dataset/final_train_reviews.txt')
path12 = os.path.expanduser('Yelp_Dataset/final_valid_reviews.txt')
path13 = os.path.expanduser('Yelp_Dataset/final_test_reviews.txt')


max_length = 20

review_list, positive_list, negative_list, neutral_list = filter_reviews(path1, max_length, 'yelp')

total_reviews = len(review_list)
print("Number of total reviews: ", total_reviews)

positive_reviews = len(positive_list)
print("Number of positive reviews: ", positive_reviews)

negative_reviews = len(negative_list)
print("Number of negative reviews: ", negative_reviews)

neutral_reviews = len(neutral_list)
print("Number of neutral reviews: ", neutral_reviews)

random.shuffle(positive_list)
random.shuffle(negative_list)
random.shuffle(neutral_list)

train_positive = positive_list[:30000]
train_negative = negative_list[:30000]
train_neutral = neutral_list[:15000]

valid_positive = positive_list[30000:35000]
valid_negative = negative_list[30000:35000]
valid_neutral = neutral_list[15000:17500]

test_positive = positive_list[35000:40000]
test_negative = negative_list[35000:40000]
test_neutral = neutral_list[17500:20000]

final_train_reviews = train_positive + train_negative + train_neutral
final_valid_reviews = valid_positive + valid_negative + valid_neutral
final_test_reviews = test_positive + test_negative + test_neutral

#write_file(train_positive, path2)
#write_file(train_negative, path3)
#write_file(train_neutral, path4)

#write_file(valid_positive, path5)
#write_file(valid_negative, path6)
#write_file(valid_neutral, path7)

#write_file(test_positive, path8)
#write_file(test_negative, path9)
#write_file(test_neutral, path10)

#write_file(final_train_reviews, path11)
#write_file(final_valid_reviews, path12)
#write_file(final_test_reviews, path13)