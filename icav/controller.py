from .tfidf import tfidf

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
        self.curPath=fpath
        try:
            with open(fpath,mode='r',encoding='utf8') as f:
                x=f.readlines()
                print('The encoding of this file is: uft-8')
                self.__proceePaper(x)
        except UnicodeDecodeError:
            try:
                with open(fpath,mode='r',encoding='gbk') as f:
                    x=f.readlines()
                    print('The encoding of this file is: gbk')
                    self.__proceePaper(x)
            except UnicodeDecodeError:
                try:
                    with open(fpath,mode='r',encoding='utf-16') as f:
                        x=f.readlines()
                        print('The encoding of this file is: utf-16')
                        self.__proceePaper(x)
                except UnicodeError:
                    with open(fpath,mode='r',encoding='iso-8859-15') as f:
                        x=f.readlines()
                        print('The encoding of this file is: iso-8859-15')
                        self.__proceePaper(x)
    
    def calculate(self):
        self.tfctr.calTFIDF()

