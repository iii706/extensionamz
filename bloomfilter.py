# 自己的简单使用
from redisbloom.client import Client,Pipeline
import redis

LIST_URL_QUEUE = "list_wait_queue"
DETAIL_URL_QUEUE = "detail_wait_queue"
LIST_URL_FILTER = 'list_url_filter'
DETSIL_URL_FILTER = 'detail_url_filter' #asin页面filter

REDIS_IP = '106.54.94.94'
REDIS_PORT = 6379
REDIS_PWD = 'foobared123'
REDIS_POOL = redis.ConnectionPool(host=REDIS_IP, port=REDIS_PORT,password=REDIS_PWD,db=0)
REDIS_CONN = redis.Redis(connection_pool= REDIS_POOL)
REDIS_BL = Client(host=REDIS_IP, port=REDIS_PORT,password=REDIS_PWD)
rets = []
for index in range(1):
    asins_ret = REDIS_CONN.srandmember(DETAIL_URL_QUEUE,number=10)
    print(asins_ret)
    ex_rets = REDIS_BL.bfMExists(DETSIL_URL_FILTER,*(i.decode() for i in asins_ret))

    for item in zip(asins_ret,ex_rets):
        print(item[1])

    #print(j)
    add_ret = REDIS_BL.bfMAdd(DETSIL_URL_FILTER, *(i.decode() for i in asins_ret))
    print(add_ret)


#
# ret1 = REDIS_BL.bfMAdd(DETSIL_URL_FILTER,*asins_ret1)
# asins_ret2 = (i.decode() for i in asins_ret)
# ret2 = REDIS_BL.bfMExists(DETSIL_URL_FILTER,*asins_ret2)
# print(ret1,ret2)





#
# # 因为我使用的是虚拟机中docker的redis, 填写虚拟机的ip地址和暴露的端口
# rb = Client(host='106.54.94.94', port=6379,password='foobared123')
# # rb.bfCreate('bloom', 0.01, 1000)
# #rb.cfCreate('urls', 1000000)
# #ret1 = rb.cfAdd('urls', 'filter')        # returns 1
# ret2 = rb.cfAddNX('urls', 'filter')      # returns 0
# ret3 = rb.cfExists('urls', 'filter')     # returns 1
# ret4 = rb.cfExists('urls', 'noexist')    # returns 0
# print(ret2,ret3,ret4)
# rb.cfDel('urls','filter')
# print(rb.cfExists('urls','filter'))

# import redis
# r = redis.Redis(host='106.54.94.94', port=6379,password='foobared123',db=0)
# ret = r.sadd('url','1','2','4')
# print(ret)
# ret = r.sadd('url','1')
# ret = r.sadd('url','苏章林')
# print(ret)
#
# counts = r.scard('url')
# print(counts)
#
# all_members = r.smembers('url')
# print(all_members)
# print(type(all_members))
# for i in all_members:
#     print(i,type(i),i.decode('utf-8'))

# print(r.srandmember('list_wait_queue').decode())
