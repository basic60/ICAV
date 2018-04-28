from os import path,listdir,getcwd
import math

corpusDir=['1','2','3']
catagory=['abstract','acknowledgement','body','conclusion','introduction','related work','whole paper']
ansiCnt=0
utf8Cnt=0
containWord={}
docList=[]
totDoc=0

class Document:
    tf={}
    tfidf={}
    totWord=0

    def __init__(self,words,tot):
        self.tf=words
        self.totWord=tot
        self.tfidf={}

    def calTFIDF(self):
        global totDoc,containWord
        for key in self.tf.keys():
            self.tf[key]= self.tf[key] / self.totWord
            if key in containWord.keys():
                self.tfidf[key]= math.log(totDoc/(1+containWord[key]))
            else:
                self.tfidf[key]= math.log(totDoc/1)
            self.tfidf[key]*=self.tf[key]

    def printHighest10(self):
        print("================================")
        print(self.totWord)
        ans=sorted(self.tfidf.items(),key=lambda d:d[1])
        for i in range(10):
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
        docList.append(Document(wd,tot))
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
        docList.append(Document(wd, tot))
        ansiCnt+=1
        f.close()


if __name__=="__main__":
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
                        fPath=path.join(cPath,k)
                        if path.isfile(fPath):
                            readFile(fPath,j)
    print("Utf8 file:"+str(utf8Cnt))
    print("ansi file:"+str(ansiCnt))

    ans={}
    for i in docList:
        i.calTFIDF()
        #print(i.totWord)
        i.printHighest10()
