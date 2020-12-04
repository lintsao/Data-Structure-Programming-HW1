# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import sys

def sortfile(path):
    index = []
    for _, file in enumerate(os.listdir(path)):
        index.append([file, int(file.replace('page', ''))])

    index = sorted(index, key = lambda s: s[1])

    return index

if __name__ == "__main__": 
    # initial  
    path = './' # save path

    # preprocess
    page_index = sortfile('web-search-files2')
    df_wordsList = pd.DataFrame(np.zeros([21, 501])).astype(str)

    for i in range(500):
        page = open(os.path.join('web-search-files2', page_index[i][0]), 'r').readlines()
        words = page[-1].replace(' \n', '').split(' ')
        for k in range(len(words)):
            df_wordsList[i][k] = words[k]
        df_wordsList[i][len(words)] = page[-1].replace(' \n', '')
    
    """# 2. Reverse index"""
    word_Reverse_index = []
    for i in range(len(df_wordsList[:-1].loc[0])): # get all words
        word_list = df_wordsList[i][:-1].sort_values(ascending=True).to_list()
        wordIn = []
        for word in word_list: # check all words
            wordIn_temp = [word]
            for j in range(len(df_wordsList[:-1].loc[0])):
                if word in df_wordsList[j][:-1].to_list():
                    wordIn_temp.append(j)
            wordIn.append(wordIn_temp)
        word_Reverse_index.append(wordIn)
        if (i + 1)%50 == 0:
            print('finish', i)

    df_word_Reverse_index = pd.DataFrame(word_Reverse_index).T

    file = open(os.path.join(path, 'reverseindex.txt'), 'w')
    words_data = []
    words_index = []
    for i in range(len(df_word_Reverse_index.loc[0]) - 1): # get all words
        for j in range(len(df_word_Reverse_index)):
            if df_word_Reverse_index[i][j][0] not in words_index: # check if words are in the list 
                words_index.append(df_word_Reverse_index[i][j][0])
                words_data.append(df_word_Reverse_index[i][j])

    words_data = sorted(words_data, key = lambda s: s[0], reverse=False)
    for i in range(len(words_data)):
        for j in range(len(words_data[i])):
            if j == 0:
                file.write('{} '.format(words_data[i][j]))  
            else:
                file.write('page{} '.format(words_data[i][j]))
        file.write('\n')
    file.close()