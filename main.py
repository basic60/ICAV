# import redis
# r=redis.Redis("127.0.0.1",'6379',decode_responses=True)
# tfidfRes=r.zrange("tfidf",0,2000,withscores=True)

# wdList=[]
# with open("wd.txt","r") as f:
#     [wdList.append(i.strip('\n')) for i in f .readlines()]

# with open("training_data.txt","a") as f:
#     for i in tfidfRes:
#         word=str(i[0]).split(":")[-1]
#         if word in wdList:
#             isterm='1'
#         else:
#             isterm='0' 
#             print(word+"=============="+str(i[0]).split(":")[0]+" "+str(i[0]).split(":")[1])

#         enval=r.zscore("entropy",i[0])
#         print("Word: "+word)
#         print("{0} 1:{1} 2:{2}".format(isterm,i[1],enval))
#         f.writelines("{0} 1:{1} 2:{2}\n".format(isterm,i[1],enval))


import icav.encoding_unifer
from os import path,getcwd
icav.encoding_unifer.unify_encoding(path.join(getcwd(),'1'))
icav.encoding_unifer.unify_encoding(path.join(getcwd(),'2'))
icav.encoding_unifer.unify_encoding(path.join(getcwd(),'3'))
