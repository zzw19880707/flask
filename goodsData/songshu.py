import requests
import json
import time
from db.conn import mongoAtlasDBConn
from db.conn import redisDBConn
# 松鼠
def getData(page):

    headers = {
                "LZADWX": "115135886063214592",
                "Content-Type": "application/json",
                "PLATFORM-TYPE":"MP",
                "LT-TOKEN": "eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50U3RhdHVzIjoxLCJhY2NvdW50SWQiOjE5Njk0ODEsImFjY291bnRUeXBlIjoid21wIiwicmVxdWVzdFVyaSI6bnVsbCwic2Vzc2lvbklkIjoiYWQ5YTA0MGMtMGE4ZS00MjRhLTlkMmYtMTQ4YmRjOWRlZDRhIiwicHJvZFR5cGUiOiJTU1BQIiwiZXhwIjoxNTU1NDg0NjEzLCJ1c2VySWQiOjExNTYxNjI3MzA4ODkyNTY5Nn0.BwKnHGjbj96mtYi9yQkMaUrfngNv5FH-ETYzWp-0Xizo6NmQeyNfE-PpKLnHCAclnzP9mfa6LXhN-ACW_j8AHA",
                "Referer": "https://servicewechat.com/wx6ff407e6b1c1f010/283/page-frame.html",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D40 MicroMessenger/7.0.3(0x17000321) NetType/4G Language/zh_CN"
            }

    requests.packages.urllib3.disable_warnings()
    result = requests.post('https://fix.songshupinpin.com/shop-community-activity/act/queryGoodsBySearch',headers =headers ,
                            # data={"communityId":"115135886063214592"},
                            data=json.dumps({"communityId":"115135886063214592","foregroundlimit":100,"foregroundIdList":'',"page":page,"pageSize":10}),
                            verify=False)

    j = json.loads(result.content.decode('utf-8'))
    r = j["body"]["activityGoodsDTOS"]
    print(r)
    if len(r) == 0 :
        return
    local_time = str(time.strftime("%Y-%m-%d", time.localtime()))
    conn = redisDBConn().db
    for d in r:
        d['local_time'] = local_time
        spuName = d['spuName']
        # 累计销售量
        soldNum = d['soldNum']
        # 价格
        price = int(d['actPrice']) / 100
        # 今日销量
        today_sold_num = 0
        if conn.exists(spuName):
            model = json.loads(conn.get(spuName))
            # 每日去重
            if model['old_time'] == local_time:
                continue
            model['old_time'] = local_time
            today_sold_num = soldNum - model['old_sold_num']
            model['old_sold_num'] = soldNum
            conn.set(spuName, json.dumps(model))
        else:
            model = {'old_time': local_time, 'old_sold_num': soldNum}
            today_sold_num = 0
            conn.set(spuName, json.dumps(model))
        d['today_sold_num'] = today_sold_num
        d['today_total_price'] = today_sold_num * price
        print(d)
        mongoAtlasDBConn().db.songshu_ervery_new.insert(d)


if __name__ == '__main__':
    getData(100)