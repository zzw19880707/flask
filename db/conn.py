import pymongo
import sys
import traceback
from db.DBConfig import MONGODB_CONFIG
from db.DBConfig import ATLASMONGODB_CONFIG
from db.DBConfig import REDISDB_CONFIG
import redis
class Singleton(object):
    # 单例模式写法,参考：http://ghostfromheaven.iteye.com/blog/1562618
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

class mongoDBonn(Singleton):
    def __init__(self):
        # connect db
        try:
            self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.db = self.conn[MONGODB_CONFIG['db_name']]  # connect db
            self.username=MONGODB_CONFIG['username']
            self.password=MONGODB_CONFIG['password']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception:
            print (traceback.format_exc())
            print ('Connect Statics Database Fail.')
            sys.exit(1)

class mongoAtlasDBConn(Singleton):
    def __init__(self):
        # connect db
        try:
            self.conn = pymongo.MongoClient("mongodb+srv://%s:%s@cluster0-1ogxa.azure.mongodb.net/test?retryWrites=true" % (ATLASMONGODB_CONFIG['username'] , ATLASMONGODB_CONFIG['password']))
            self.db = self.conn.Mypython  # connect db
        except Exception:
            print (traceback.format_exc())
            print ('Connect Statics Database Fail.')
            sys.exit(1)

class redisDBConn(Singleton):
    def __init__(self):
        # connect db
        try:
            self.pool = redis.ConnectionPool(host=REDISDB_CONFIG['host'], port=REDISDB_CONFIG['port'], password=REDISDB_CONFIG['PASSWORD'], decode_responses=True)
            self.db = redis.Redis(connection_pool=self.pool)
        except Exception:
            print (traceback.format_exc())
            print ('Connect Statics Database Fail.')
            sys.exit(1)