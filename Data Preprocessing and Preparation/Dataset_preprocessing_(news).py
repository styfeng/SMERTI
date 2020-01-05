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


def filter_text(path, max_length):
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


def write_file(lst, path):
    f = io.open(path, "w", encoding = 'utf-8')
    print("Currently writing lines to file ...")
    f.writelines(lst)
    f.close()
    print("Lines successfully written to file!")


path1 = os.path.expanduser('News_Dataset/News_Category_Dataset_v2.json')
path2 = os.path.expanduser('News_Dataset/transformer_data/train_headlines.txt')
path3 = os.path.expanduser('News_Dataset/transformer_data/val_headlines.txt')
path4 = os.path.expanduser('News_Dataset/transformer_data/test_headlines.txt')

max_length = 20

headline_list = filter_text(path1, max_length)
total_headlines = len(headline_list)
print("Total number of headlines: ", total_headlines)

random.shuffle(headline_list)

train_list = headline_list[:120000]
val_list = headline_list[120000:140000]
test_list = headline_list[140000:160000]

#write_file(train_list, path2)
#write_file(val_list, path3)
#write_file(test_list, path4)