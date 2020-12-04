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
    d = sys.argv[1] # d_value
    DIFF = sys.argv[2] # DIFF_value
    d = float(d)
    DIFF = float(DIFF)
    mode = sys.argv[3] # check mode: input mode or other
    path = './' # save path

    # preprocess
    page_index = sortfile('web-search-files2')
    pointList = np.zeros([501, 501])
    df_wordsList = pd.DataFrame(np.zeros([21, 501])).astype(str)

    for i in range(len(pointList) - 1):
        page = open(os.path.join('web-search-files2', page_index[i][0]), 'r').readlines()
        for j in range(len(page[:-2])): # get all pages pointed
            pointedPage = int(page[j].replace('page', '').replace('\n', ''))
            pointList[pointedPage][i] = 1/len(page[:-2])
        words = page[-1].replace(' \n', '').split(' ')
        for k in range(len(words)):
            df_wordsList[i][k] = words[k]
        df_wordsList[i][len(words)] = page[-1].replace(' \n', '')
    print('finish preprocessing')

    # compute page rank
    diff = np.inf
    pr = np.ones([501, 1])/501
    while diff >= DIFF:
        pr_before = pr
        pr = (1 - d)/501 + d*np.matmul(pointList, pr)
        diff = np.sum(abs(pr_before - pr))
    pr = pd.DataFrame(pr)
    pr.columns = ['d: ' + str(d) + ' DIFF: ' + str(DIFF)]
    print('finish page rank')

    """# 3. Search engine"""
    if mode != 'input': # summit_mode for list.txt
        read_file = open(os.path.join(path, 'list.txt'), 'r').readlines() # read list.txt
        file = open(os.path.join(path, 'result_{}_{}.txt'.format(int(d*100), '%03d' % int(DIFF*1000))), 'w')
        for line in range(len(read_file)):
            input_words_list = read_file[line].replace('\n', '').split(' ')
            AND = []
            OR = []
            for i in range(len(df_wordsList[:-1].loc[0])):
                And = True
                for word in input_words_list:
                    if word not in df_wordsList[i][:-1].to_list():
                        And = False
                    else:
                        if i not in OR:
                            OR.append([i, pr['d: ' + str(d) + ' DIFF: ' + str(DIFF)][i]])
                if And == True:
                    AND.append([i, pr['d: ' + str(d) + ' DIFF: ' + str(DIFF)][i]])
            AND = np.array(sorted(AND, key = lambda s: s[1], reverse=True)[:10])[:, 0].astype(int) if len(AND) > 0 else np.array([-1])
            OR = np.array(sorted(OR, key = lambda s: s[1], reverse=True)[:10])[:, 0].astype(int) if len(OR) > 0 else np.array([-1])
            if len(input_words_list) == 1:
                for page in AND:
                    file.write('page{} '.format(str(page)) if AND[0] != -1 else 'none')
                file.write('\n')
            else:
                file.write('AND ')
                for page in AND:
                    file.write('page{} '.format(str(page)) if AND[0] != -1 else 'none')
                file.write('\n')
                file.write('OR ')
                for page in OR:
                    file.write('page{} '.format(str(page)) if OR[0] != -1 else 'none')
                file.write('\n')
        file.close()
        print('save file')
    else: # input_mode for interaction
        input_words = '' # initial input value
        while input_words != 'end': # stop until input is 'end' 
            input_words = input('Please input some words：')
            input_words_list = input_words.split(' ')
            print('your input words:', input_words_list)
            if input_words != 'end':
                AND = []
                OR = []
                for i in range(len(df_wordsList[:-1].loc[0])):
                    And = True
                    for word in input_words_list:
                        if word not in df_wordsList[i][:-1].to_list():
                            And = False
                        else:
                            if i not in OR:
                                OR.append([i, pr['d: ' + str(d) + ' DIFF: ' + str(DIFF)][i]])
                    if And == True:
                        AND.append([i, pr['d: ' + str(d) + ' DIFF: ' + str(DIFF)][i]])

                AND = np.array(sorted(AND, key = lambda s: s[1], reverse=True)[:10])[:, 0].astype(int) if len(AND) > 0 else 'none'
                OR = np.array(sorted(OR, key = lambda s: s[1], reverse=True)[:10])[:, 0].astype(int) if len(OR) > 0 else 'none'
                print(input_words)
                if len(input_words_list) > 1:
                    print('AND', end = ' ')
                    for page in AND:
                        print('page{} '.format(str(page)) if AND[0] != -1 else 'none', end = ' ')
                    print('')
                    print('OR', end = ' ')
                    for page in OR:
                        print('page{} '.format(str(page)) if OR[0] != -1 else 'none', end = ' ')
                    print('')
                else:
                    for page in AND:
                        print('page{} '.format(str(page)) if AND[0] != -1 else 'none', end = ' ')
                    print('')