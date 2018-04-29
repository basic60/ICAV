from os import path,listdir,getcwd
import math

corpusDir=['1','2','3']
catagory=['abstract','acknowledgement','body','conclusion','introduction','related work','whole paper']
ansiCnt=0
utf8Cnt=0
containWord={}
docList=[]
totDoc=0

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

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
        for key in self.tf.keys():
            self.tf[key]= self.tf[key] / self.totWord
            if key in containWord.keys():
                self.tfidf[key]= math.log(totDoc/(1+containWord[key]))
            else:
                self.tfidf[key]= math.log(totDoc/1)
            self.tfidf[key]*=self.tf[key]

    def printHighest(self):
        print("================================")
        print(self.filePath)
        print(self.totWord)
        ans=sorted(self.tfidf.items(),key=lambda d:d[1])
        for i in range(30):
            print(ans[i])
        print("================================")


def readFile(fpath,cate="whole paper"):
    global utf8Cnt,ansiCnt,docList,totDoc,containWord
    totDoc+=1
    flag=0
    wd = {}
    try:
        f=open(fpath,mode='r',encoding='utf8')
        tot=0
        for i in f.readlines():
            for j in i.split():
                if j!='' and j in wd:
                    wd[j]+=1
                elif j!='' and j not in wd:
                    wd[j]=1

                if flag==0 and j not in containWord:
                    containWord[j]=1
                    flag=1
                elif flag==0 and j not in containWord:
                    containWord[j]+=1
                    flag=1
                tot+=1
        docList.append(Document(wd,tot,fpath))
        utf8Cnt+=1
        f.close()
    except UnicodeDecodeError:
        f=open(fpath,mode='r',encoding='ANSI')
        tot = 0
        for i in f.readlines():
            for j in i.split():
                if j!='' and j in wd:
                    wd[j]+=1
                elif j!='' and j not in wd:
                    wd[j]=1

                if flag==0 and j not in containWord:
                    containWord[j]=1
                    flag=1
                elif flag==0 and j not in containWord:
                    containWord[j]+=1
                    flag=1
                tot+=1
        docList.append(Document(wd, tot,fpath))
        ansiCnt+=1
        f.close()


class res:
    txt=""
    value=0

    def __init__(self,txt,val):
        self.txt=txt
        self.value=val

test=["1.txt","2.txt","3.txt","4.txt","5.txt","6.txt","7.txt","8.txt","9.txt","10.txt"]

if __name__=="__main__":
    cor=[]
    nameList=[]
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
                            totDoc += 1
                            flag = 0
                            try:
                                f = open(fPath, mode='r', encoding='utf8')
                                stmp=""
                                for i in f.readlines():
                                    stmp+=" "
                                    stmp+=i
                                cor.append(stmp)
                                nameList.append(fPath)
                                utf8Cnt += 1
                                f.close()
                            except UnicodeDecodeError:
                                f = open(fPath, mode='r', encoding='ansi')
                                stmp=""
                                for i in f.readlines():
                                    stmp+=" "
                                    stmp+=i
                                cor.append(stmp)
                                utf8Cnt += 1
                                nameList.append(fPath)
                                f.close()

    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(cor))
    word=vectorizer.get_feature_names()
    weight=tfidf.toarray()

    cnt=0
    for i in range(len(weight)):
        print("---------------------------------------------------------------")
        print(nameList[cnt])
        cnt+=1
        resList = []

        for j in range(len(word)):
            resList.append(res(word[j],weight[i][j]))
        ans=sorted(resList,key=lambda d:d.value,reverse=True)


        for j in range(20):
            print(str(ans[j].txt)+" "+str(ans[j].value))

    # flist=listdir()
    # for i in flist:
    #     if path.isdir(i) and i in corpusDir:
    #         corpusPath=path.join(getcwd(),i)
    #         clist=listdir(corpusPath)
    #         for j in clist:
    #             cPath=path.join(corpusPath,j)
    #             if path.isdir(cPath) and j=='whole paper':
    #                 print("Read data from " + cPath)
    #                 for k in listdir(cPath):
    #                     fPath=path.join(cPath,k)
    #                     if path.isfile(fPath):
    #                         readFile(fPath,j)
    # print("Utf8 file:"+str(utf8Cnt))
    # print("ansi file:"+str(ansiCnt))
    #
    # ans={}
    # print(len(docList))
    # for i in range(10):
    #     docList[i].calTFIDF()
    #     docList[i].printHighest()
