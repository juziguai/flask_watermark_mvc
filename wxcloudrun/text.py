"""
Created on Sun Oct 23 19:35:01 2016
@author:
"""
from random import randint

all_yuming_max = {
    'v1-cold.douyinvod.com',
    'v26-cold.douyinvod.com', 'v26-hon.douyinvod.com', 'v5-f-gzcm06.douyinvod.com', 'v5-gdgz-a.douyinvod.com',
    'v93.douyinvod.com', 'v5-che.douyinvod.com', 'v6-qos-hourly.douyinvod.com', 'v26-che.douyinvod.com',
    'v6-cold.douyinvod.com', 'v83-x.douyinvod.com', 'v5-coldb.douyinvod.com', 'v3-z.douyinvod.com',
    'v1-x.douyinvod.com', 'v6-ab-e1.douyinvod.com', 'v5-abtest.douyinvod.com', 'v9-che.douyinvod.com',
    'v83-y.douyinvod.com', 'v5-litea.douyinvod.com', 'v3-che.douyinvod.com', 'v29-cold.douyinvod.com',
    'v5-lite.douyinvod.com', 'v29-qos-control.douyinvod.com', 'v5-gdgz.douyinvod.com', 'v5-ttcp-a.douyinvod.com',
    'v3-b.douyinvod.com', 'v9-z-qos-control.douyinvod.com', 'v9-x-qos-hourly.douyinvod.com', 'v9-chc.douyinvod.com',
    'v9-qos-hourly.douyinvod.com', 'v5-ttcp-b.douyinvod.com', 'v6-z-qos-control.douyinvod.com', 'v5-dlyd.douyinvod.com',
    'v5-coldy.douyinvod.com', 'v3-c.douyinvod.com', 'v5-jbwl.douyinvod.com', 'v26-0015c002.douyinvod.com',
    'v5-gdwy.douyinvod.com', 'v3-d.douyinvod.com', 'v3-p.douyinvod.com', 'v5-gdhy.douyinvod.com',
    'v26-cold.douyinvod.com', 'v5-lite-a.douyinvod.com', 'v5-i.douyinvod.com', 'v5-g.douyinvod.com',
    'v26-qos-daily.douyinvod.com', 'v5-dash.douyinvod.com', 'v5-h.douyinvod.com', 'v5-f.douyinvod.com',
    'v3-a.douyinvod.com', 'v83.douyinvod.com', 'v5-cold.douyinvod.com', 'v3-y.douyinvod.com', 'v26-x.douyinvod.com',
    'v27-ipv6.douyinvod.com', 'v9-ipv6.douyinvod.com', 'v5-yacu.douyinvod.com', 'v29-ipv6.douyinvod.com',
    'v26-coldf.douyinvod.com', 'v5.douyinvod.com', 'v11.douyinvod.com', 'v6-z.douyinvod.com', 'v1.douyinvod.com',
    'v9-y.douyinvod.com', 'v9-z.douyinvod.com', 'v9.douyinvod.com', 'v3-x.douyinvod.com', 'v6-y.douyinvod.com',
    'v3-ipv6.douyinvod.com', 'v5-e.douyinvod.com', 'v3.douyinvod.com', 'v6-ipv6.douyinvod.com', 'v9-x.douyinvod.com',
    'v6-p.douyinvod.com', 'v1-2p.douyinvod.com', 'v1-p.douyinvod.com', 'v1-ipv6.douyinvod.com', 'v24.douyinvod.com',
    'v1-dy.douyinvod.com', 'v6.douyinvod.com', 'v6-x.douyinvod.com', 'v26-ipv6.douyinvod.com', 'v27.douyinvod.com',
    'v92.douyinvod.com', 'v95.douyinvod.com', 'douyinvod.com', 'v26.douyinvod.com', 'v29.douyinvod.com'
}

x = randint ( 0, 300 )
print ( 'x=', x )

frequency = 6
print ( '您最多有',frequency,'次猜数字的机会' )
for i in range ( frequency ):
    r = input ()
    if r not in all_yuming_max:
        print("匹配失败")
        print ( '猜大了,还剩', frequency - i - 1 )
    else:
        print ( '匹配成功' )
        break
print ( '猜数字游戏已结束' )
