###################
#定时任务执行类
###################
from pytz import utc
from datetime import datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
class apstask():
    def __int__(self):
        '''实例化APS'''
        jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }
        executors = {
            'default': ThreadPoolExecutor(max_workers=30),
            'processpool': ProcessPoolExecutor(max_workers=30)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        self.apstask=BackgroundScheduler()
    def start(self):
        '''运行'''
        self.apstask.start()
    def shutdown(self):
        '''关闭'''
        self.apstask.shutdown()
    def add(self):
        '''添加job'''
        next_minute = (datetime.now() + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
        next_run_time = datetime.strptime(next_minute, "%Y-%m-%d %H:%M")
        self.apstask.add_job(
                hehe,
                trigger='interval',
                seconds=3,
                id="qwerrr",
                kwargs=["222222222"],
                next_run_time=next_run_time,
        )
    def remove_job(self,id):
        '''移除job'''
        self.apstask.remove_job(id)

def hehe(info):
    print("111111111:"+info)





