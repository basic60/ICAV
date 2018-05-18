from icav.controller import Controller
from os import path,listdir,getcwd

corpusDir=['1','2','3']
category=['whole paper']
command=1

if command==1:
    ctr=Controller()
    for i in listdir():
        if path.isdir(i) and i in corpusDir:
            ptmp=path.join(getcwd(),i)
            print(ptmp)
            for j in listdir(ptmp):
                ftmp=path.join(ptmp,j)   
                if path.isdir(ftmp) and j in category:
                    for k in listdir(ftmp):
                        filePath=path.join(ftmp,k)
                        if path.isfile(filePath):
                            ctr.addPaper(filePath)
    print("Adding corpus finished! Starting process...")
    ctr.calculate()
    print("Finished!")
else:
    pass
