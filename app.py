from flask import Flask


from flask_apscheduler import APScheduler
from flask import current_app
import redis
import time

app = Flask(__name__)

scheduler = APScheduler();
scheduler.init_app(app)
scheduler.start()

@app.route('/test')
def test():
    test()

    return '你好帅哦'

@app.route('/')
def hello_world():
    # scheduler = APScheduler();
    # scheduler.init_app(app)
    # scheduler.start()


    host = 'localhoredis-10684.c1.asia-northeast1-1.gce.cloud.redislabs.comst'
    port = 10685
    PASSWORD = 'VUnd8roSLg2v5R9pX6apCsODHbwdSdVG'
    # pool = redis.ConnectionPool( host = host, port = port, password = PASSWORD, decode_responses=True )

    # r = redis.Redis(host=host, port=port, password = PASSWORD)
    # r = redis.Redis(connection_pool=pool)
    # r.set('k12', 'tttttt')
    # r.lpush('test',str(time.time()))

    return 'Hello World!'
def add_job():
    print(str(time.time()))
def test():
    job = {
        'id': 'rds-to-mysql-1',  # 任务的唯一ID，不要冲突
        'func': 'add_job',  # 执行任务的function名称
        'args': '',  # 如果function需要参数，就在这里添加
    };
    # current_app 是获取当前的app主体
    #
    # 网上没找到这句代码，这是我穷途末路的时候，不小心按到了Ctrl + APScheduler()，
    # 看到他的源码里的init_app()方法里面，将sched实例注入到了app里面，
    # 才突然发现新大陆，解决了这个问题
    # 这些add_job的参数名称，可以借鉴：http://www.dannysite.com/blog/73/
    result = current_app.apscheduler.add_job(func=__name__ + ':' + job['func'], id=job['id'], trigger='interval',
                                             seconds=1);
    print(result);

if __name__ == '__main__':
    app.run()
