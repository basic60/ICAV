class Controller:
    def __init__(self):
        self.totPaper=0

    def __processWord(self,s):
        slist=list(s)
        ret=""
        for i in range(len(slist)):
            if s[i]>='a' and s[i]<='z' or s[i]>='A' and s[i]<='Z':
                ret+=s[i]
        return ret.lower()

    def __proceePaper(self,val):
        for line in val:
            wlist=line.split(' ')
            wlist=[self.__processWord(i) for i in wlist]

    def addPaper(self,fpath):
        print("Start process"+fpath)
        self.totPaper+=1
        try:
            with open(fpath,mode='r',encoding='utf8') as f:
                x=f.readlines()
                self.__proceePaper(x)
        except UnicodeDecodeError:
            try:
                with open(fpath,mode='r',encoding='gbk') as f:
                    x=f.readlines()
                    self.__proceePaper(x)
            except UnicodeDecodeError:
                try:
                    with open(fpath,mode='r',encoding='utf-16') as f:
                        x=f.readlines()
                        self.__proceePaper(x)
                except UnicodeError:
                    with open(fpath,mode='r',encoding='iso-8859-15') as f:
                        x=f.readlines()
                        self.__proceePaper(x)