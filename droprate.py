import csv

def readCSV( path ):
    csvfile = file(path,'rb')
    return csvfile

def writeCSV( path ):
    csvfile = open(path,'wb')
    return csvfile

def putIntodict1(reader,reader2):
    d1 = {}
    d2 = {}
    for line in reader:
        if line[0] == "enrollment_id":
            continue
        d2[(line[0])] = line[2]
        d1[line[2]] = {}
        d1[line[2]]["allnum"] = 0
        d1[line[2]]["dropnum"] = 0
    for line in reader2:
        if line[0] == "enrollment_id":
            continue
        d2[(line[0])] = line[2]
        d1[line[2]] = {}
        d1[line[2]]["allnum"] = 0
        d1[line[2]]["dropnum"] = 0
    print "finish putting"
    return d1,d2


def count(reader,user,course ):
    for line in reader:
        course[user[line[0]]]["allnum"] += 1
        if line[1] == "1":
            course[user[line[0]]]["dropnum"] += 1
    for key in course:
        course[key]["dropnum"] = float(course[key]["dropnum"])/course[key]["allnum"]
    return course
    
if __name__ == '__main__':
    en_train = readCSV("enrollment_train.csv")
    en_test = readCSV("enrollment_test.csv")
    course,user = putIntodict1( csv.reader(en_train), csv.reader(en_test))
    dropout = readCSV("truth_train.csv")
    course = count( csv.reader(dropout),user,course )
    output = writeCSV("dropout.csv")
    for i in user:
        data = [ i,course[user[i]]["dropnum"] ]
        csv.writer(output).writerow(data)
    en_train.close()
    dropout.close()
    output.close()
