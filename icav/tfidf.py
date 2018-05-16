import math
import redis

class paperStatistic:
    def __init__(self):
        self.wordCnt={}
        self.totWord=0

    def addWord(self,word):
        self.totWord+=1
        if word in self.wordCnt:
            self.wordCnt[word]+=1
        else:
            self.wordCnt[word]=0

class tfidf:
    def __init__(self):
        self.totPaper=0
        self.paperList=[]
        self.wordApp={}
        self.r=redis.Redis('127.0.0.1','6379',decode_responses=True)
        

    def addPaper(self,wdList):
        self.totPaper+=1
        staob=paperStatistic()
        flag=[]
        for i in wdList:
            if i not in flag:
                flag.append(i)
                if not i in self.wordApp:
                    self.wordApp[i]=1
                else:
                    self.wordApp[i]+=1
            staob.addWord(i)
        self.paperList.append(staob)           
                    
    def calTFIDF(self):
        pipe=self.r.pipeline()
        for i in self.paperList:
            for j in i.wordCnt:
                wd=j
                tf=i.wordCnt[j]/i.totWord
                idf= math.log(self.totPaper/(1+self.wordApp[j]))
                tfidf=tf*idf
                print(str(tfidf)+" "+wd)
                pipe.zadd("tfidf",tfidf,wd)
        pipe.execute()






