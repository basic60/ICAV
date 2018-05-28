from icav.controller import Controller
from os import path,listdir,getcwd
from libsvm.python.svmutil import *
from libsvm.python.svm import *
import matplotlib.pyplot as plt
import redis

corpusDir=['1','2','3']
category=['whole paper']
command=0

if command==0:
    ctr=Controller()

    r=redis.Redis("127.0.0.1",'6379',decode_responses=True)
    if not r.exists("tfidf"):
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

    sx=[]
    sy=[]
    fx=[]
    fy=[]
    with open("training_data.txt","r") as f:
        for line in f.readlines():
            s=line.split()
            label.append(int(s[0]))
            
            v1=s[1].split(":")[1]    
            dicn={}        
            dicn[1]=float(v1)

            print(s[0])
            if s[0]=='0':
                fx.append(float(v1))
            else:
                sx.append(float(v1))
            
            v1=s[2].split(":")[1]            
            dicn[2]=float(v1)

            if s[0]=='0':
                fy.append(float(v1))
            else:
                sy.append(float(v1))

            vector.append(dicn)
    
    fig=plt.figure()
    ax1=fig.add_subplot(111)
    ax1.set_title("hhh")
    plt.xlabel('tfidf')
    plt.ylabel('entropy')
    ax1.scatter(fx[:100],fy[:100],c='r')
    ax1.scatter(sx[:100],sy[:100],c='g')
    plt.show()
    


    prob=svm_problem(label[:100],vector[:100])
    param = svm_parameter('-t 0 -c 0.03125 -g 0.0078125')
    model = svm_train(prob,param)



    svm_save_model("model.txt",model)

    
    yt = [0]
    xt = [{1:0.92852715503839881, 2:0.056472306067509255}]
    print(label)
    print("=====================")
    p_label, p_acc, p_val = svm_predict(label, vector, model)
    print(p_label)
    print(p_val)
    print("=====================")
    
