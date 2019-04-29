from flask import Flask


from flask_apscheduler import APScheduler
from flask import current_app
import time
from db.conn import mongoAtlasDBConn
from db.conn import redisDBConn
app = Flask(__name__)

scheduler = APScheduler();
scheduler.init_app(app)
scheduler.start()

@app.route('/test')
def test():
    # test()
    return '你好帅哦'

@app.route('/menu')
def menu():
    # scheduler = APScheduler();
    # scheduler.init_app(app)
    # scheduler.start()

    print(redisDBConn().db.get('25°3橙【1份1.4kg】'))


    print(mongoAtlasDBConn().db.songshu_ervery_new.find())
    return 'Hello World!' + \
           '</br><a href=/test>政哥你好帅</a>' + \
           '</br><a href=/test>貔貅你好帅</a>' + \
           '</br><a href=/test>李政你好帅</a>'

@app.route('/')
def hello_world():
    return ''

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
