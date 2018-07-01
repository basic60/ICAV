class Reader:
    def readlines(self,filePath):
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