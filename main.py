from os import path,listdir,getcwd
import math
import sys

corpusDir=['1','2','3']
catagory=['abstract','acknowledgement','body','conclusion','introduction','related work','whole paper']
ansiCnt=0
utf8Cnt=0
containWord={}
docList=[]
totDoc=0

finResult=[]

class Result:
    word=""
    tf=0
    idf=0
    tfidf=0

    def __init__(self,word,tf,idf,tfidf):
        self.word=word
        self.tf=tf
        self.idf=idf
        self.tfidf=tfidf

class Document:
    tf={}
    tfidf={}
    totWord=0
    filePath=""

    def __init__(self,words,tot,fpath):
        self.tf=words
        self.totWord=tot
        self.tfidf={}
        self.filePath=fpath

    def calTFIDF(self):
        global totDoc,containWord
        
        tmp=[]
        for key in self.tf.keys():
            self.tf[key]= self.tf[key] / self.totWord
            if key in containWord.keys():
                self.tfidf[key]= math.log(totDoc/(1+containWord[key]))
            else:
                self.tfidf[key]= math.log(totDoc/1)

            self.tfidf[key]*=self.tf[key]

            tmp.append(Result(key,self.tf[key],self.tfidf[key]/self.tf[key],self.tfidf[key]))
        tmp=sorted(tmp,key=lambda x:x.tfidf,reverse=True)
        finResult.extend(tmp)

def processStr(s):
    slist=list(s)
    ret=""
    for i in range(len(slist)):
        if s[i]>='a' and s[i]<='z' or s[i]>='a' and s[i]<='z':
            ret+=s[i]
    return ret.lower()


def readFile(fpath,cate="whole paper"):
    global utf8Cnt,ansiCnt,docList,totDoc,containWord
    print("read "+fpath)
    totDoc+=1
    flag=[]
    wd = {}
    try:
        f=open(fpath,mode='r',encoding='utf8')
        tot=0
        for i in f.readlines():
            for j in i.split():
                stmp=processStr(j)
                if stmp=='':
                    continue 

                if stmp!='' and stmp in wd:
                    wd[stmp]+=1
                elif stmp!='' and stmp not in wd:
                    wd[stmp]=1

                if stmp not in flag:
                    if stmp not in containWord:
                        containWord[stmp]=1
                    else:                    
                        containWord[stmp]+=1
                    flag.append(stmp)
                
                tot+=1
        docList.append(Document(wd,tot,fpath))
        utf8Cnt+=1
        f.close()
    except UnicodeDecodeError:
        try:
            print("try gbk")
            with open(fpath,mode='r',encoding='gbk') as f:
                tot = 0
                for i in f.readlines():
                    for j in i.split():
                        stmp=processStr(j)
                        if stmp=='':
                            continue 

                        if stmp!='' and stmp in wd:
                            wd[stmp]+=1
                        elif stmp!='' and stmp not in wd:
                            wd[stmp]=1

                        if stmp not in flag:
                            if stmp not in containWord:
                                containWord[stmp]=1
                            else:                    
                                containWord[stmp]+=1
                            flag.append(stmp)
                        tot+=1
                docList.append(Document(wd, tot,fpath))
                ansiCnt+=1
        except UnicodeDecodeError:
            try:
                print("try utf-16")
                with open(fpath,mode='r',encoding='utf-16') as f:
                    tot = 0
                    for i in f.readlines():
                        for j in i.split():
                            stmp=processStr(j)
                            if stmp=='':
                                continue 

                            if stmp!='' and stmp in wd:
                                wd[stmp]+=1
                            elif stmp!='' and stmp not in wd:
                                wd[stmp]=1

                            if stmp not in flag:
                                if stmp not in containWord:
                                    containWord[stmp]=1
                                else:                    
                                    containWord[stmp]+=1
                                flag.append(stmp)
                            tot+=1
                    docList.append(Document(wd, tot,fpath))
                    ansiCnt+=1
            except UnicodeError:
                print("try iso-8859-15")
                with open(fpath,mode='r',encoding='iso-8859-15') as f:
                    tot = 0
                    for i in f.readlines():
                        for j in i.split():
                            stmp=processStr(j)
                            if stmp=='':
                                continue 

                            if stmp!='' and stmp in wd:
                                wd[stmp]+=1
                            elif stmp!='' and stmp not in wd:
                                wd[stmp]=1

                            if stmp not in flag:
                                if stmp not in containWord:
                                    containWord[stmp]=1
                                else:                    
                                    containWord[stmp]+=1
                                flag.append(stmp)
                            tot+=1
                    docList.append(Document(wd, tot,fpath))
                    ansiCnt+=1

class res:
    txt=""
    value=0

    def __init__(self,txt,val):
        self.txt=txt
        self.value=val

test=["1.txt","2.txt","3.txt","4.txt","5.txt","6.txt","7.txt","8.txt","9.txt","79.txt"]
stwList=[]

if __name__=="__main__":
    fs=open("stopwords.txt","r")
    for i in fs.readlines():
        stwList.append(i)
    fs.close()

    flist=listdir()
    for i in flist:
        if path.isdir(i) and i in corpusDir:
            corpusPath=path.join(getcwd(),i)
            clist=listdir(corpusPath)
            for j in clist:
                cPath=path.join(corpusPath,j)
                if path.isdir(cPath) and j=='whole paper':
                    print("Read data from " + cPath)
                    for k in listdir(cPath):
                        if k not in test:
                           continue
                        fPath=path.join(cPath,k)
                        if path.isfile(fPath):
                            readFile(fPath,j)
    print("Utf8 file:"+str(utf8Cnt))
    print("ansi file:"+str(ansiCnt))
    
    for i in range(len(docList)):
        docList[i].calTFIDF()
    ans=sorted(finResult,key=lambda d:d.tfidf,reverse=True)
    for i in range(len(ans)):
        if i>500:
            break
        if ans[i].word in stwList:
            print("stop words: "+ans[i].word)
            continue
        print("Word:%-20s TF:%-10.5f  IDF:%-10.5f  TF-IDF:%-10.5f "%(ans[i].word,ans[i].tf,ans[i].idf,ans[i].tfidf))
        # print(ans[i].word+"TF:"+str(ans[i].tf)+" IDF:"+str(ans[i].idf)+" TFIDF:"+str(ans[i].tfidf))