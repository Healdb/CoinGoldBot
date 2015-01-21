#coding: utf-8
import os
import csv

def delete_line(bad_words, fn):
    with open(fn+'.txt') as oldfile, open(fn + '2.txt', 'w+') as newfile:
        for line in oldfile:
            if not all(bad_word in line for bad_word in bad_words):
                newfile.write(line)
        newfile.close()
    with open(fn + '2.txt') as oldfile, open(fn + '.txt', 'w+') as newfile:
        for line in oldfile:
            newfile.write(line)
        newfile.close()
        os.remove(fn + '2.txt')
def saveDict(dict1, fn):
    f = open(fn, 'ab+')
    w = csv.writer(f)
    for key, val in dict1.items():
        w.writerow([key, val])
    f.close()
def readDict(fn):
    f = open(fn, "r")
    dict1={}
    for key, val in csv.reader(f):
        dict1[key] = val
    f.close()
    return(dict1)
