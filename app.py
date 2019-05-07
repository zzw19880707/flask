from flask import Flask
from flask_apscheduler import APScheduler
from flask import current_app
from goodsData.start import getSongshuTodayData
from goodsData.start import songshuStartTask
from goodsData.start import timerTask
from flask_mail import Mail,Message
import threading
from db.conn import mongoAtlasDBConn
from db.conn import redisDBConn
app = Flask(__name__)

# 定时器持久化
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
jobstores = {
    'redis': RedisJobStore(connection_pool=redisDBConn().pool),#用redis作backend
}
executors = {
    'default': ThreadPoolExecutor(10),#默认线程数
    'processpool': ProcessPoolExecutor(3)#默认进程
}
# from apscheduler.schedulers.background import BackgroundScheduler
# sched = BackgroundScheduler(jobstores=jobstores, executors=executors)
app.config['SCHEDULER_JOBSTORES']=jobstores
app.config['SCHEDULER_EXECUTORS']=executors
# 定时器
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# 邮箱
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'zzw__8877@126.com'
app.config['MAIL_PASSWORD'] = 'shazi31'
mail = Mail(app)

from flask import g

def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f

@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        response = callback(response)
    return response

@app.route('/test')
def test():
    return '你好帅哦'

@app.route('/menu')
def menu():
    # print(redisDBConn().db.get('25°3橙【1份1.4kg】'))
    # print(mongoAtlasDBConn().db.songshu_ervery_new.find())
    return 'Hello World!' + \
           '</br><a href=/test>政哥你好帅</a>' + \
           '</br><a href=/test>貔貅你好帅</a>' + \
           '</br><a href=/test>李政你好帅</a>' + \
           '</br><a href=/songshuloaddata>获取松鼠今日数据</a>'+ \
           '</br><a href=/gettask>获取运行中的任务</a>'+ \
           '</br><a href=/starttask>启动任务</a>'+ \
           '</br><a href=/songshulist>松鼠</a>'

@app.route('/songshuloaddata')
def songshuloaddata():
    getSongshuTodayData()
    return ''

@app.route('/')
def hello_world():
    return '你好'

@app.route('/starttask')
def start_task():
    songshuStartTask()
    timerTask()
    return '启动成功'

@app.route('/gettask')
def  get_task() :#获取
    jobs=scheduler.get_jobs(jobstores)
    j = '<table>'
    j += ('<tr><td>%s</td><td>%s</td></tr>' % ('名字' , 'id'))
    for job in jobs:
        j += ('<tr><td>%s</td><td>%s</td></tr>' % (job.name , job.id))
    j += '</table>'
    return j
@app.route('/songshulist')
def  songshu_list() :
    results = mongoAtlasDBConn().db.songshu_ervery_new.aggregate([{'$group':{'_id':'$local_time','count':{'$sum':1}}},{'$sort':{'_id':1}}])
    j = '<table border=1>'
    j += ('<tr><td>%s</td><td>%s</td></tr>' % ('时间' , '商品数'))
    for result in results:
        print(result)
        j += ('<tr><td>%s</td><td>%s</td></tr>' % (result['_id'] , result['count']))
    j += '</table>'
    return j

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

msg = Message('标题', sender='zzw__8877@126.com', recipients=['zzw414851474@qq.com'])
@app.route('/send_email')
def send_email():
    msg.body = '内容'
    thread = threading.Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return 'success'

def test():
    print("test")
if __name__ == '__main__':
    app.run()
