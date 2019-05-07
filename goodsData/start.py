from goodsData.songshu import getData
from flask import current_app
import requests
def getSongshuTodayData():
    for i in range(1,100):
        b = getData(i)
        if not b:
            break

def songshuStartTask():
    job = {
        'id': 'rds-to-mysql-1',  # 任务的唯一ID，不要冲突
        'func': 'getSongshuTodayData',  # 执行任务的function名称
        'args': '',  # 如果function需要参数，就在这里添加
    };
    # current_app 是获取当前的app主体
    #
    # 网上没找到这句代码，这是我穷途末路的时候，不小心按到了Ctrl + APScheduler()，
    # 看到他的源码里的init_app()方法里面，将sched实例注入到了app里面，
    # 才突然发现新大陆，解决了这个问题
    # 这些add_job的参数名称，可以借鉴：http://www.dannysite.com/blog/73/
    result = current_app.apscheduler.add_job(func=__name__ + ':' + job['func'], id=job['id'], trigger='interval',
                                             hours = 2 ,jobstore='redis' , replace_existing=True)
    print(result)




def keepAvailable():
    print('keepAvailable')
    requests.get('https://flask0428.herokuapp.com/test')


def timerTask():
    job = {
        'id': 'keep-available-task',  # 任务的唯一ID，不要冲突
        'func': 'keepAvailable',  # 执行任务的function名称
        'args': '',  # 如果function需要参数，就在这里添加
    };

    result = current_app.apscheduler.add_job(func=__name__ + ':' + job['func'], id=job['id'], trigger='interval',
                                             minutes = 15 ,jobstore='redis', replace_existing=True)
    print(result)

