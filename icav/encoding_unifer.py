from .reader import Reader
from os import listdir,path,getcwd
import queue
def unify_encoding(dirPath):
    r=Reader()
    q=queue.Queue()
    [q.put(i) for i in listdir(dirPath)]
    cpath=getcwd()
    while not q.empty():
        x=q.get()
        if path.isfile(x):
            lines=r.readlines(x)
            with open(x,'w') as f:
                f.writelines(lines)
        else:
            nxtPath=path.join(x,)


            


