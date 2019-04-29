import urllib.request
import re
import random
import time
import os
# import pymysql
from db.conn import mongoAtlasDBConn

# 用户协议
uas = []

def getIpFromNetwork(db,cursor):
    url="http://www.xicidaili.com/nn/"
    date = time.strftime("%Y-%m-%d", time.localtime())
    for i in range(1,4):
        url+=str(i)
        req = urllib.request.Request(url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0")
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
        # re1=re.compile(r"(([01]{0,1}\d{0,1}[0-9]|2{0,1}[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}[0-9]|2[0-4]\d|25[0-5])</td>\n(\s){1,}<td>\d{1,5}")
        re1 = re.compile(r"(([01]{0,1}\d{0,1}[0-9]|2{0,1}[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}[0-9]|2[0-4]\d|25[0-5])</td>\n(\s){1,}<td>\d{1,5}</td>\n(\s){1,}<td>\n(\s){1,}(.*)\n(\s){1,}<\/td>\n(\s){1,}(.*)\n(\s){1,}<td>(HTTP|HTTPS)</td>")
        for each_ip in re.finditer(re1,html):
            s = each_ip.group()
            http = s.find('HTTPS')
            ip = s.replace("</td>\n      <td>",":",1)
            a = ip.find('<')
            ip = ip[:a]
            ip = ip.split(':')
            print(ip)
            t = ''
            if http > 0 :
                t = 'HTTPS'
            else:
                t = 'HTTP'
            sql = 'INSERT INTO proxy(type,ip,port,date) VALUES ( \'%s\' , \'%s\' , \'%s\' , \'%s\')' % (t, ip[0],ip[1],date)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print('插入成功')
            except Exception as e:
                # 如果发生错误则回滚
                db.rollback()




def updateIp():
    # 打开数据库连接
    db = pymysql.connect(host = "127.0.0.1", user = "root", passwd = "", db = "mysql")



    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from proxy order by rand() limit 1"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()

        if results == None:
            print('暂无数据')

        else:
            http = results[1]
            ip = results[2]
            port = results[3]
            # 打印结果
            # print("type=%s,ip=%s,port=%s" % (http, ip, port))
            return {http : ip + ':' + port}
    except:

        print("Error: unable to fetch data")

    getIpFromNetwork(db, cursor)



# def getIp():
#     list = updateIp()
#     return random.choice(list)





def LoadUserAgents(i):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    global uas
    if len(uas) == 0 :
        with open(i, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    uas.append(ua.strip()[1:-1 - 1])
    return {'User-Agent' : random.choice(uas)}


def updateIpFromMongoDB():
    my_conn = mongoAtlasDBConn()
    collection_count = my_conn.db['IpProxy'].find().count()
    if collection_count == 0:
        # 无数据
        getIpFromNetworkIntoMongoDB()
        result = my_conn.db['IpProxy'].find_one()
        return {result['type'] : result['ip'] +':' + result['prot'] }
    else:
        result = my_conn.db['IpProxy'].find_one({'random':random.randint(0 ,collection_count)})
        return {result['type'] : result['ip'] +':' + result['prot'] }

def getIpFromNetworkIntoMongoDB():
    url="http://www.xicidaili.com/nn/"
    date = time.strftime("%Y-%m-%d", time.localtime())
    index = 0
    for i in range(1,4):
        url+=str(i)
        req = urllib.request.Request(url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0")
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
        # re1=re.compile(r"(([01]{0,1}\d{0,1}[0-9]|2{0,1}[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}[0-9]|2[0-4]\d|25[0-5])</td>\n(\s){1,}<td>\d{1,5}")
        re1 = re.compile(r"(([01]{0,1}\d{0,1}[0-9]|2{0,1}[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}[0-9]|2[0-4]\d|25[0-5])</td>\n(\s){1,}<td>\d{1,5}</td>\n(\s){1,}<td>\n(\s){1,}(.*)\n(\s){1,}<\/td>\n(\s){1,}(.*)\n(\s){1,}<td>(HTTP|HTTPS)</td>")
        for each_ip in re.finditer(re1,html):
            s = each_ip.group()
            http = s.find('HTTPS')
            ip = s.replace("</td>\n      <td>",":",1)
            a = ip.find('<')
            ip = ip[:a]
            ip = ip.split(':')
            print(ip)
            t = ''
            if http > 0 :
                t = 'HTTPS'
            else:
                t = 'HTTP'
            index += 1
            mongoAtlasDBConn().db['IpProxy'].insert_one( {'type':t , 'ip':ip[0] ,'prot':ip[1] , 'date':date , 'random': index})

if __name__ == '__main__':

    # updateIp()
    ip = updateIpFromMongoDB()
    print(ip)
    # print(getIp())
    # print('获取到的IP ：' + getIp())

    # print(LoadUserAgents('user_agents.txt'))
    # for x in list:
        # print(x ,end= '\n')
