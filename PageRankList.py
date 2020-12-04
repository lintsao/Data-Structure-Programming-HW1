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
    path = './' # save path

    # preprocess
    page_index = sortfile('web-search-files2')
    pointList = np.zeros([501, 501])
    countList = np.zeros([501, 1])
    df_wordsList = pd.DataFrame(np.zeros([21, 501])).astype(str)

    for i in range(len(pointList) - 1):
        page = open(os.path.join('web-search-files2', page_index[i][0]), 'r').readlines()
        for j in range(len(page[:-2])): # get all pages pointed
            pointedPage = int(page[j].replace('page', '').replace('\n', ''))
            pointList[pointedPage][i] = 1/len(page[:-2])
            countList[i] = len(page[:-2])
        words = page[-1].replace(' \n', '').split(' ')
        for k in range(len(words)):
            df_wordsList[i][k] = words[k]
        df_wordsList[i][len(words)] = page[-1].replace(' \n', '')

    df_countList = pd.DataFrame(countList) 
    df_countList.columns = ['count']  
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

    """# 1. Page Rank list"""
    file = open(os.path.join(path, 'pr_{}_{}.txt'.format(int(d*100), '%03d' % int(DIFF*1000))), 'w')
    name = 'd: ' + str(d) + ' DIFF: ' + str(DIFF)
    df = pd.concat([pr[name][:-1], df_countList[:-1]], axis=1).sort_values(by=([name]), ascending=False)
    for line in range(len(df)):
        file.write('page{} {} {}'.format(
            df[name].index[line], int(df['count'][df[name].index[line]]), str('%.7f'%df[name][df[name].index[line]])[1:]))
        file.write('\n')
    file.close()
    print('save file')
