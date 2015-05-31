# -*- coding: cp936 -*-
'''
wusiyuan
生成训练用的特征值
'''
import csv
import random
import time
'''-----------------------------------特征-------------------------------------'''
global login_times
global login_morning
global login_afternoon
global login_evening
global nagivate
global access
global problem
global video
global page_close
global wiki
global discussion
global server
global browser
global browser
global deep_degree
login_times = 1
login_morning = 2
login_afternoon = 3
login_evening = 4
nagivate = 5
access  = 6
problem = 7
video = 8
page_close = 9
wiki = 10
discussion = 11
server = 12
browser = 13
deep_degree = 14

def readCSV( path ):
    csvfile = file(path,'r')
    return csvfile

def writeCSV( path ):
    csvfile = open(path,'w')
    return csvfile

# object文件，父节点，子节点关系
def put2dict( reader):
    dic_father = {}
    for line in reader:
        l = line[3].split(' ')
        for i in l:
             dic_father[i] = line[1]
    print "dict created"
    return dicfa

# 计算子节点的深度
def deep(father,key):
    d = 0
    while (key in father):
        key = father[key]
        d = d + 1
    return d

# 特征值存放list初始化
def initialize(reader):
    l = [0]*201000
    for line in reader:
        if line[0] == "enrollment_id":
            continue
        user = int(line[0])
        l[user] = []
        l[user].append(user)
        for i in range(0,14):
            l[user].append(0)
    print "finish initializing"
    return l
        
def dataAnalysis(reader, lis, father):
    for line in reader:
        if line[0] == "enrollment_id":
            continue
        hour = int((line[1].split('T')[-1]).split(':')[0])
        user = int(line[0])
        lis[user][login_times] = lis[user][login_times] + 1
        # 登陆的时间
        if hour >= 6 and hour <12:
            lis[user][login_morning] = lis[user][login_morning] + 1
        if hour >= 12 and hour <18:
            lis[user][login_afternoon] = lis[user][login_afternoon] + 1
        if hour >= 18 or hour <6:
            lis[user][login_evening] = lis[user][login_evening] + 1
        source = line[2]
        # 浏览的source
        if source == "browser":
            lis[user][browser] = lis[user][browser] + 1
        else:
            lis[user][server] = lis[user][server] + 1
        # event 计数
        event = line[3]
        if event =="nagivate":
            lis[user][nagivate] = lis[user][nagivate] + 1
        if event =="access":
            lis[user][access] = lis[user][access] + 1
        if event =="problem":
            lis[user][problem] = lis[user][problem] + 1
        if event =="video":
            lis[user][video] = lis[user][video] + 1
        if event =="page_close":
            lis[user][page_close] = lis[user][page_close] + 1
        if event =="wiki":
            lis[user][wiki] = lis[user][wiki] + 1
        if event =="discussion":
            lis[user][discussion] = lis[user][discussion] + 1
        # 浏览的深度求和
        lis[user][deep_degree] = lis[user][deep_degree] + deep(father, line[4])
    print "finish analysising"
    return lis

def write2csv(lis, writer):
    for i in lis:
        if i == 0:
            continue
        # 基本就是各个值求平均， 但是最后要不要放到 data里 都是可选的
        morning_login_rate = float(i[login_morning])/i[login_times]
        afternoon_login_rate = float(i[login_afternoon])/i[login_times]
        evening_login_rate = float(i[login_evening])/i[login_times]
        nagivate_rate = float(i[nagivate])/i[login_times]
        access_rate = float(i[access])/i[login_times]
        problem_rate = float(i[problem])/i[login_times]
        video_rate = float(i[video])/i[login_times]
        page_close_rate = float(i[page_close])/i[login_times]
        wiki_rate = float(i[wiki])/i[login_times]
        discussion_rate = float(i[discussion])/i[login_times]
        browser_rate = float(i[browser])/i[login_times]
        server_rate = float(i[browser])/i[login_times]
        frequent = float(i[login_times])/100
        deep_rate = float(i[deep_degree])/i[login_times]
        data = [i[0],frequent,morning_login_rate,afternoon_login_rate,
                evening_login_rate,nagivate_rate,access_rate,problem_rate,
                video_rate,wiki_rate,discussion_rate,browser_rate,deep_rate]
        writer.writerow( data )
    print "finish writing"
    

if __name__ == '__main__':
    start = time.time()
    obj = readCSV("object.csv")
    father = put2dict( csv.reader(obj) )
    csvfilefolder = {1:["enrollment_test.csv","log_test.csv","test.csv"],2:["enrollment_train.csv","log_train.csv","train.csv" ]}
    for key in csvfilefolder:
        user = readCSV(csvfilefolder[key][0])
        log = readCSV(csvfilefolder[key][1])
        output = writeCSV(csvfilefolder[key][2])
        user_info = initialize( csv.reader(user))
        user_info = dataAnalysis( csv.reader(log), user_info, father)
        write2csv( user_info, csv.writer(output ))
        user.close()
        log.close()
        output.close()
    finish = time.time()
    print (finish - start)/60
    '''
1:["enrollment_test.csv","log_test.csv","test.csv"],
    '''
