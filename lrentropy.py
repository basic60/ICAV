import math
class lrentropy:
    wlist=[]
    def __processWord(self,s):
        slist=list(s)
        ret=""
        for i in range(len(slist)):
            if s[i]>='a' and s[i]<='z' or s[i]>='A' and s[i]<='Z' or i=='-':
                ret+=s[i]
        return ret.lower()

    def add_paper(self,fpath):
        with open(fpath,'r') as f:
            for line in f.readlines():
                self.wlist.extend(list(filter(lambda x:x!='',[self.__processWord(i) for i in line.split(' ')])))

    def lrent(self,word):
        try:
            dic={}
            dicr={}
            st=-1
            totl=totr=0
            while True:
                st=self.wlist.index(word,st+1)
                if st>0:
                    if self.wlist[st-1] in dic:
                        dic[self.wlist[st-1]]+=1
                    else:
                        dic[self.wlist[st-1]]=1
                    totl+=1
                if st+1<len(self.wlist):
                    if self.wlist[st+1] in dicr:
                        dicr[self.wlist[st+1]]+=1
                    else:
                        dicr[self.wlist[st+1]]=1
                    totr+=1
        except ValueError:
            ans=0
            for i in dic:
                px=dic[i]/totl
                ans+=-px*math.log(px)
            print("L Entropy: "+str(ans))
            ans=0
            for i in dicr:
                px=dicr[i]/totr
                ans+=-px*math.log(px)
            print("R Entropy: "+str(ans))

if __name__=='__main__':
    a=lrentropy()
    a.add_paper("1.txt")
    a.lrent("is")