from icav.controller import Controller
from os import path,listdir,getcwd
from libsvm.python.svmutil import *
from libsvm.python.svm import *

corpusDir=['1','2','3']
category=['whole paper']
command=0

if command==1:
    ctr=Controller()
    for i in listdir():
        if path.isdir(i) and i in corpusDir:
            ptmp=path.join(getcwd(),i)
            print(ptmp)
            for j in listdir(ptmp):
                ftmp=path.join(ptmp,j)   
                if path.isdir(ftmp) and j in category:
                    for k in listdir(ftmp):
                        filePath=path.join(ftmp,k)
                        if path.isfile(filePath):
                            ctr.addPaper(filePath)
    print("Adding corpus finished! Starting process...")
    ctr.calculate()
    print("Finished!")
else:
    print("Start traning model!")
    label=[]
    vector=[]
    with open("training_data2.txt","r") as f:
        for line in f.readlines():
            s=line.split()
            label.append(int(s[0]))
            
            v1=s[1].split(":")[1]    
            dicn={}        
            dicn[1]=float(v1)
          #  v1=s[2].split(":")[1]            
          #  dicn[2]=float(v1)
            print(dicn)
            vector.append(dicn)
    prob=svm_problem(label[:200],vector[:200])
    param = svm_parameter('-t 2 -c 4.4 -b 1')
    model = svm_train(prob,param)
    
    
    yt = [0]
    xt = [{1:0.02852715503839881, 2:0.056472306067509255}]
    print(label)
    print("=====================")
    p_label, p_acc, p_val = svm_predict(label, vector, model)
    print(p_label)
    print("=====================")
    
