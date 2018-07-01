from .reader import Reader
from os import listdir,path,getcwd,walk
import queue

def unify_encoding(targetPath):
    r=Reader()
    for dirPath,dirName,fileName in walk(targetPath):
        if fileName!=[]:
            for i in fileName:
                finPath=path.join(dirPath,i)
                lines=r.readlines(finPath)
                with open(finPath,'w') as f:
                    f.writelines(lines)





            


