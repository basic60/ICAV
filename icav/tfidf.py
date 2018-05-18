import math
import redis

def _generateKey(fpath):
    return ':'.join([str(fpath).split('/')[-3],str(fpath).split('/')[-1]])

class paperStatistic:
    def __init__(self,fpath):
        self.wordCnt={}
        self.totWord=0
        self.fpath=fpath
        self.r=redis.Redis('127.0.0.1','6379',decode_responses=True)
        

    def addWord(self,word):
        if word in self.wordCnt:
            self.wordCnt[word]+=1
            self.r.zincrby("word_cnt",_generateKey(self.fpath)+":"+word,1)            
        else:
            self.wordCnt[word]=1
            self.r.zadd("word_cnt",_generateKey(self.fpath)+":"+word,1)

class tfidf:
    def __init__(self):
        self.totPaper=0
        self.paperList=[]
        self.wordApp={}
        self.r=redis.Redis('127.0.0.1','6379',decode_responses=True)
         
    def addPaper(self,wdList,fpath):
        self.totPaper+=1

        staob=paperStatistic(fpath)
        staob.totWord=len(wdList)
        self.r.zadd("paper_word_count",_generateKey(fpath),staob.totWord)
        
        flag=[]
        for i in wdList:
            if i not in flag:
                flag.append(i)
                if  i not in self.wordApp:
                    self.wordApp[i]=1
                    self.r.zadd("paper_contain_word",i,1)
                else:
                    self.wordApp[i]+=1
                    self.r.zincrby("paper_contain_word",i,1)
            staob.addWord(i)
        self.paperList.append(staob)           
                    
    def calTFIDF(self):
        self.r.set("totPaper",self.totPaper)
        pipe=self.r.pipeline()
        for pid in self.paperList:
            for wd in pid.wordCnt:
                tf=pid.wordCnt[wd]/pid.totWord
                idf= math.log(self.totPaper/(1+self.wordApp[wd]))
                tfidf=tf*idf
                pipe.zadd("tfidf",_generateKey(pid.fpath)+":"+wd,tfidf)
                pipe.zadd("entropy",_generateKey(pid.fpath)+":"+wd,-1*tf*math.log(tf,2))
                
        pipe.execute()






