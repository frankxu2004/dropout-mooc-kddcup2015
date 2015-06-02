# -*- coding: cp936 -*-
import csv
import numpy as np
import pandas as pd
import time
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.svm import LinearSVR
from sklearn.ensemble import RandomForestClassifier

def readCSV( path ):
    csvfile = file(path,'rb')
    return csvfile

def writeCSV( path ):
    csvfile = file(path,'wb')
    return csvfile
#用作映射。。但是发现效果不好暂时没用
def mapp(lis, p, q):
    lis2 = []
    for i in lis:
        adjust = (i[1]-p)/(q-p)
        if adjust<0.00000001:
            adjust = 0
        data = [ i[0],adjust]
        lis2.append(data)
    print "finish mapping"
    return lis2
#把 输入的特征X全部塞进一个List里面。。sklearn 模型里统一的格式
def putXIntolist(reader):
    l = []
    for line in reader:
        row = []
        line1 = line[1:]
        for i in line1:
            row.append( float(i) )
        l.append(row)
    print "finish putting"
    return l
#把 Y 全部塞进一个List里面。。sklearn 模型里统一的格式
def putYIntolist(reader):
    l = []
    for line in reader:
        l.append( float(line[1]) )
    print "finish putting"
    return l
# 最后需要分类的值 也塞进一个list里
def putTestIntolist(reader):
    l = []
    for line in reader:
        row = []
        row.append(int(line[0]))
        for i in line[1:]:
            row.append( float(i) )
        l.append(row)
    return l

def machineLearning(X_parameters,Y_parameters,  predict_value):
    clf1 = LinearSVR()   # svm for regression
    clf2 = LinearRegression() 
    clf1.fit(X_parameters, Y_parameters)
    clf2.fit(X_parameters, Y_parameters)
    print "finish fitting"
    answer = []
    max = 0
    min = 1
    for line in predict_value:
        line1 = line[1:]
        predict_outcome1 = clf1.predict(line1)
        predict_outcome2 = clf2.predict(line1)
        # 数据要求 [0,1]
        if predict_outcome1[0]>1:
            predict_outcome1[0]=1
        if predict_outcome1[0]<0:
            predict_outcome1[0]=0
        if predict_outcome2[0]>1:
            predict_outcome2[0]=1
        if predict_outcome2[0]<0:
            predict_outcome2[0]=0
        data = [line[0],(predict_outcome1[0]+predict_outcome2[0])*0.5]
        answer.append(data)
    print "finish learning"
    return answer, max,min
    
    
if __name__ == '__main__':
    start = time.time()
    train_x = readCSV("train.csv")
    train_y = readCSV("truth_train.csv")
    test = readCSV("test.csv")
    outcome = writeCSV("outcome.csv")
    x_parameter = putXIntolist( csv.reader(train_x) )
    y_parameter = putYIntolist( csv.reader(train_y) )
    test_parameter = putTestIntolist( csv.reader(test) )
    ans,ma,mi = machineLearning(x_parameter,y_parameter, test_parameter)
    #ans = mapp(ans,ma,mi)
    for i in ans:
        (csv.writer(outcome)).writerow(i)
    train_x.close()
    train_y.close()
    test.close()
    outcome.close()
    finish = time.time()
    print (finish - start)/60
        
