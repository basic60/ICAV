import redis
r=redis.Redis("127.0.0.1",'6379',decode_responses=True)
tfidfRes=r.zrange("tfidf",0,2000,withscores=True)

wdList=[]
with open("wd.txt","r") as f:
    [wdList.append(i.strip('\n')) for i in f .readlines()]

with open("training_data.txt","a") as f:
    for i in tfidfRes:
        word=str(i[0]).split(":")[-1]
        if word in wdList:
            isterm='1'
        else:
            isterm='0' 
            print(word+"=============="+str(i[0]).split(":")[0]+" "+str(i[0]).split(":")[1])

        enval=r.zscore("entropy",i[0])
        print("Word: "+word)
        print("{0} 1:{1} 2:{2}".format(isterm,i[1],enval))
        f.writelines("{0} 1:{1} 2:{2}\n".format(isterm,i[1],enval))
# f=open("123123.txt",'r',encoding='utf-16')
# x=f.readline()
# print(x)
# f2=open("99.txt",'w')
# f2.write(x)
# f2.close()
# f.close()