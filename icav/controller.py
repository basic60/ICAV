from .tfidf import tfidf
from .reader import Reader

class Controller:
    def __init__(self):
        self.tfctr=tfidf()

    def __processWord(self,s):
        slist=list(s)
        ret=""
        for i in range(len(slist)):
            if s[i]>='a' and s[i]<='z' or s[i]>='A' and s[i]<='Z' or i=='-':
                ret+=s[i]
        return ret.lower()

    def __proceePaper(self,val):
        wlist=[]
        for line in val:
            wlist.extend(list(filter(lambda x:x!='',[self.__processWord(i) for i in line.split(' ')])))
        self.tfctr.addPaper(wlist,self.curPath)

    def addPaper(self,fpath):
        print("Start process: "+fpath)
        rd=Reader()
        self.curPath=fpath

        x=rd.readlines(fpath)
        self.__proceePaper(x)
    
    def calculate(self):
        self.tfctr.calTFIDF()

