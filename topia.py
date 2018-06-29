#!/usr/bin/python
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
                    # if '_' in k:
                    #     remove(filePath)
                    print(filePath)
                    ans=''
                    with open(filePath,mode='r') as f:
                        txt=f.readlines()
                        for i in txt:
                            ans+=i
                    ans=extractor(ans)
                    f2name=str(k).split('.')[0]+'_'+str(k).split('.')[0]+".txt"
                    with open(path.join(ftmp,f2name),mode='w') as f:
                        f.writelines([i[0]+'\n'for i in ans])






# f=open("./1/whole paper/2.txt",mode="r")
# test=f.readlines()
# ans=''
# for i in test:
#     ans+=i
# ret=extractor(ans)
# print(i[0] for i in ret)
# for i in ret:
#     print(i[0])
