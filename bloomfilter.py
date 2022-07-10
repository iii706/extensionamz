# 自己的简单使用
from redisbloom.client import Client
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

import redis
r = redis.Redis(host='106.54.94.94', port=6379,password='foobared123',db=0)
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

print(r.srandmember('list_wait_queue').decode())
