import datetime
def get_time_by_nexttime(task_time):
    '''获取定时任务运行时间下次执行日期'''
    num=datetime.datetime.now()
    numss=num-datetime.datetime.strptime(task_time,"%Y-%m-%d:%H")
    day = int(numss.days % 365)
    if day>=100:
        return 0
    else:
        return day + 1


def time_add(current_data,num):
    '''日期相加的方法'''
    if isinstance(current_data,str):
        current_data=datetime.datetime.strptime(current_data,"%Y-%m-%d:%H")
    return current_data+num

if __name__ == '__main__':
    import os
    from AutoTestPlatform.settings import BASE_DIR
    print(os.path.join(BASE_DIR))
