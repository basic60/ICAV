import redis
r=redis.Redis("127.0.0.1",'6379',decode_responses=True)

with open("namedatabase.txt",'r') as f:
    for i in f.readlines():
        nm=list(filter(lambda x:x>='a' and x<'z' or x>='A' and x<='Z',i))
        r.zadd('person_name',''.join(nm),1)