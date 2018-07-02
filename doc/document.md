# 基于topia和tfidf的术语抽取工具
## 前言
术语（terminology）是在特定学科领域用来表示概念的称谓的集合。而如何从论文中抽取出术语，正是本工具的目的。本工具采取了基于语言规则的第三方库[topia](https://pypi.org/project/topia.termextract/),并且同时计算出文件的tfidf值，用于过滤不合理结果，最终达到术语抽取的效果。

项目完整源码：https://github.com/basic60/ICAV

## 项目具体实现和代码分析
### 一、开发环境配置
本项目的开发平台是ubuntu 18.04。采用python3编写，然而因为topia只支持python2，因此部分代码采用pyton2编写。请先确定安装了如下软件：
- Python2
- Python3
- Redis

之后把语料库和topia库解压到项目的根目录,环境就配置完成了（目录结构可见附录）。

### 二、读取文件数据
在配置完了开发环境之后，就可以进行开发了。想要抽取术语，第一步自然就是把文件读取到内存之中。然而遗憾的是，这一切并不是只调用open和readlines等函数就可以了。因为有一个很麻烦的问题就是文件的编码格式各不相同。有utf-8,utf-16,iso-8859-15,gbk等各种五花八门的格式。因此我们要做的第一步就是先把文件的格式统一，这样之后处理起来会方便很多。

首先尝试出文件正确的编码：
```
class Reader:
    def readlines(self,filePath):                                           # 尝试正确的编码并且返回读取结果
        try:
            with open(filePath,mode='r',encoding='utf8') as f:
                x=f.readlines()
                print('The encoding of '+str(filePath)+' is: uft-8')
                return x
        except UnicodeDecodeError:
            try:
                with open(filePath,mode='r',encoding='gbk') as f:
                    x=f.readlines()
                    print('The encoding of '+str(filePath)+' is: gbk')
                    return x
            except UnicodeDecodeError:
                try:
                    with open(filePath,mode='r',encoding='utf-16') as f:
                        x=f.readlines()
                        print('The encoding of '+str(filePath)+' is: utf-16')
                        return x
                except UnicodeError:
                    with open(filePath,mode='r',encoding='iso-8859-15') as f:
                        x=f.readlines()
                        print('The encoding of '+str(filePath)+' is: iso-8859-15')
                        return x
```
不难看出，该函数会返回文件的读取结果。之后我们再把这些文件统一保存成utf-8的格式，以便之后的处理，代码下：
```
def unify_encoding(targetPath):
    r=Reader()
    for dirPath,dirName,fileName in walk(targetPath): # 遍历目标目录下的所有文件
        if fileName!=[]:
            for i in fileName:
                finPath=path.join(dirPath,i)
                lines=r.readlines(finPath)     # 使用Reader对象尝试正确编码并读取结果
                with open(finPath,'w') as f:
                    f.writelines(lines)        # 统一保存成utf-8格式
```

### 三、计算tfidf值
TF-IDF（term frequency–inverse document frequency）是一种用于信息检索与数据挖掘的常用加权技术。TF意思是词频(Term Frequency)，IDF意思是逆文本频率指数(Inverse Document Frequency)。

在一份给定的文件里，词频（term frequency，tf）指的是某一个给定的词语在该文件中出现的频率,即用词语出现的次数除以文档中的总词数。

逆向文件频率（inverse document frequency，IDF）是一个词语普遍重要性的度量。某一特定词语的IDF，可以由总文件数目除以包含该词语之文件的数目，再将得到的商取对数得到。

最后将TF值与IDF值相乘，就得到了TF-IDF的结果，即：TF-IDF=TF*IDF。TF-IDF值能够在一定程度上反映一个词语能够带给你的信息大小，他不是单单依靠词语的出现频率来决定一个词语的重要程度，在引入了IDF之后，一些高频词语但又在每篇文档中都出现的词语，比如说’is‘,'the'等的TF-IDF值将会很低。而仅在少数文档中多次出现的词语将会有较高的TF-IDF值，这也是多数术语所拥有的特征。

代码实现如下：
```
from .tfidf import tfidf
from .reader import Reader

class Controller:
    def __init__(self):
        self.tfctr=tfidf()

    def __processWord(self,s):
        slist=list(s)
        ret=""
        for i in range(len(slist)):
            if s[i]>='a' and s[i]<='z' or s[i]>='A' and s[i]<='Z' or i=='-':    # 去除特殊符号
                ret+=s[i]
        return ret.lower()

    def __proceePaper(self,val):
        wlist=[]
        for line in val:
            wlist.extend(list(filter(lambda x:x!='',[self.__processWord(i) for i in line.split(' ')]))) # 预处理文件
        self.tfctr.addPaper(wlist,self.curPath)

    def addPaper(self,fpath):
        print("Start process: "+fpath)
        rd=Reader()
        self.curPath=fpath

        x=rd.readlines(fpath)
        self.__proceePaper(x)
    
    def calculate(self):
        self.tfctr.calTFIDF()   # 计算tfidf值
```
这段代码做的是，将文件进行预处理，去除文档中无用的特殊符号。
你应该已经注意到了，负责计算TFIDF值的是tfidf类，接下来我们再来看看tfidf类的代码：
```
import math
import redis

def _generateKey(fpath):
    return ':'.join([str(fpath).split('/')[-3],str(fpath).split('/')[-1]])  # 产生Redis的键。（eg.‘1:1.txt:the’,这个键表示语料库一中1.txt里‘the’这个词语的相关数据）

class paperStatistic:                                                       # 统计对象，以文档为单位，包含了词语总数和某个词语出现次数等信息。
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
         
    def addPaper(self,wdList,fpath):                           # 对一篇文章的相关信息进行统计
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
                    self.r.zincrby("paper_contain_word",i,1)    # paper_contain_word表示包含某个词语的文档总数
            staob.addWord(i)                                    # 一个文档中词语的总数
        self.paperList.append(staob)                            # 添加统计对象
                    
    def calTFIDF(self):
        self.r.set("totPaper",self.totPaper)
        pipe=self.r.pipeline()
        for pid in self.paperList:
            for wd in pid.wordCnt:
                tf=pid.wordCnt[wd]/pid.totWord                              # 计算TF值
                idf= math.log(self.totPaper/(1+self.wordApp[wd]))           # 计算IDF值
                tfidf=tf*idf                                                # 计算TF-IDF值
                pipe.zadd("tfidf",_generateKey(pid.fpath)+":"+wd,tfidf)
                pipe.zadd("entropy",_generateKey(pid.fpath)+":"+wd,-1*tf*math.log(tf,2))
        pipe.execute()                                                      # 运行流水线，执行redis命令
```
这段代码的作用就是统计文档中词语的出现频率，并且计算出相应的TF值和IDF值(顺便也计算了一下信息熵)，最后计算出TFIDF值。并且使用Redis存储数据。

### 四、使用topia
在完成了对于TF-IDF值的计算之后，下一步要做的就是使用第三方库topia。文档地址：https://pypi.org/project/topia.termextract/

因为topia只支持python2，因此**下面这段代码用python2编写**：
```
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from topia.termextract import extract
from os import listdir,path,getcwd,remove
corpusDir=['1','2','3']
category=['whole paper']


extractor = extract.TermExtractor()
extractor.filter = extract.permissiveFilter

for i in listdir(getcwd()):
    if path.isdir(i) and i  in corpusDir:
        ptmp=path.join(getcwd(),i)
        for j in listdir(ptmp):
            ftmp=path.join(ptmp,j)
            if path.isdir(ftmp) and j in category:
                for k in listdir(ftmp):
                    filePath=path.join(ftmp,k)
                    print(filePath)
                    ans=''
                    with open(filePath,mode='r') as f:
                        txt=[line.decode('utf-8') for line in f.readlines()] # 读取文件内容
                        for i in txt:
                            ans+=i
                    ans=extractor(ans)  # 抽取术语
                    f2name=str(k).split('.')[0]+'_'+str(k).split('.')[0]+".txt" # 生成结果文件的文件名。
                    with open(path.join(ftmp,f2name),mode='w') as f:
                        f.writelines([(i[0]+'\n').encode(encoding='utf8') for i in ans]) # 将结果统一保存为utf-8格式。
```
运行之后就可以得出抽取的结果。

### 五、得出最终结果
在以上步骤都完成之后，就是最后一步了，因为单单使用topia或者单单使用tpidf进行术语抽取的结果并不理想，因此这里我们采用的方法是把这两种方法进行结合，对于topia抽取的结果，检查其TF-IDF值，
过滤掉TF-IDF低于阈值的结果，并且去掉人名，特殊符号等明显不合理的结果。

代码如下：
```
    r=redis.Redis("127.0.0.1",'6379',decode_responses=True)
    for i in listdir():
        if path.isdir(i) and i in corpusDir:
            ptmp=path.join(getcwd(),i)
            for j in listdir(ptmp):
                ftmp=path.join(ptmp,j)   
                if path.isdir(ftmp) and j in category:
                    for k in listdir(ftmp):
                        if '_' in k:                # 仅对topia抽取的结果文件进行处理。
                            if k not in limit:
                                continue

                            filePath=path.join(ftmp,k)
                            rd=Reader()
                            for lines in rd.readlines(filePath):    # 读取文件
                                wd=lines.split(' ')

                                def __processWord(s):   # 预处理函数
                                    slist=list(s)
                                    ret=""
                                    for ii in range(len(slist)):
                                        if s[ii]>='a' and s[ii]<='z' or s[ii]>='A' and s[ii]<='Z' or s[ii]=='-':
                                            ret+=s[ii]
                                        elif s[ii]=='\n':
                                            pass
                                        else:
                                            return ''
                                    if len(ret)<2:
                                        return ''
                                    return ret
                                
                                wd=list(filter(lambda x:x!='',[__processWord(i) for i in wd]))   # 对抽取结果进行预处理，处理特殊符号。

                                cnt=0
                                for item in wd:
                                    if r.zrank('person_name',item)!=None:
                                        cnt+=1
                                if cnt==len(wd):
                                    continue    # 排除人名结果

                                if len(wd)==1:
                                    query=str(i)+':'+k.split('_')[0]+".txt:"+wd[0].lower() # 生成对于tfidf值的查询
                                    ret=r.zscore("tfidf",query)
                                    if ret and ret>0.001:                                   # 排除tfidf过低的结果
                                        print(wd[0])
                                elif len(wd)>1:
                                    for item in wd:
                                        print(item,end=' ')
                                    print()
```
在上面的代码之中我们提到了排除人名答案，本项目使用到的数据地址：http://www.quietaffiliate.com/free-first-name-and-last-name-databases-csv-and-sql/

添加数据库代码如下：
```
import redis
r=redis.Redis("127.0.0.1",'6379',decode_responses=True)

with open("namedatabase.txt",'r') as f:
    for i in f.readlines():
        nm=list(filter(lambda x:x>='a' and x<'z' or x>='A' and x<='Z',i))
        r.zadd('person_name',''.join(nm),1)
```

## 附录
### 项目目录结构
.
├── 1

│   └── whole paper

|    ├── xx.txt
 
├── 2

│   └── whole paper

|    ├── xx.txt

├── 3

│   └── whole paper

|    ├── xx.txt

├── ans.txt

├── doc

│   └── document.md

├── icav

│   ├── controller.py

│   ├── controller.pyc

│   ├── encoding_unifer.py

│   ├── __init__.py

│   ├── reader.py

│   ├── tfidf.py

│   └── tfidf.pyc

├── LICENSE

├── lrentropy.py

├── main.py

├── model.txt

├── namedatabase.txt

├── person_name.py

├── stopwords.txt

├── test.py

├── test.txt

├── topia

│   ├── __init__.py

│   └── termextract

│       ├── data

│       │   └── english-lexicon.txt

│       ├── example.txt

│       ├── extract.py

│       ├── extract.pyc

│       ├── __init__.py

│       ├── interfaces.py

│       ├── interfaces.pyc

│       ├── README.txt

│       ├── tag.py

│       ├── tag.pyc

│       ├── tests.py

│       ├── timeout.py

│       └── timeout.pyc

├── topia.py

├── training_data2.txt

├── training_data.txt

└── wd.txt

### Reids键名字
- "word_cnt"
- "paper_word_count"
- "totPaper"
- "person_name"
- "paper_contain_word"
- "tfidf"
- "entropy"
