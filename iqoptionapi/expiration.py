#python
import time
from datetime import datetime,timedelta

 

def get_expiration_time(timestamp,duration):
    #
    now_date = datetime.fromtimestamp(timestamp)
    exp_date=now_date.replace(second=0,microsecond=0)
    if (int((exp_date+timedelta(minutes=1)).timestamp())-timestamp)>30:
        exp_date= exp_date+timedelta(minutes=1)
    
    else:
        exp_date= exp_date+timedelta(minutes=2)
    exp=[]
    for _ in range(5):
        exp.append(exp_date.timestamp())
        exp_date= exp_date+timedelta(minutes=1)
    
    

    idx=50
    index=0
    now_date = datetime.fromtimestamp(timestamp)
    exp_date=now_date.replace(second=0,microsecond=0)
    while index<idx:
        if int(exp_date.strftime("%M"))%15==0 and (int(exp_date.timestamp())-int(timestamp))>60*5:
            exp.append(exp_date.timestamp())
            index=index+1
        exp_date= exp_date+timedelta(minutes=1)

    remaning=[]
     
    for t in exp:
        remaning.append(int(t)-int(time.time()))

    close = [abs(x-60*duration) for x in remaning]
     
    return int(exp[close.index(min(close))]),int(close.index(min(close)))
 

def get_remaning_time(timestamp):
    now_date = datetime.fromtimestamp(timestamp)
    exp_date=now_date.replace(second=0,microsecond=0)
    if (int((exp_date+timedelta(minutes=1)).timestamp())-timestamp)>30:
        exp_date= exp_date+timedelta(minutes=1)

    else:
        exp_date= exp_date+timedelta(minutes=2)
    exp=[]
    for _ in range(5):
        exp.append(exp_date.timestamp())
        exp_date= exp_date+timedelta(minutes=1)
    idx=11
    index=0
    now_date = datetime.fromtimestamp(timestamp)
    exp_date=now_date.replace(second=0,microsecond=0)
    while index<idx:
        if int(exp_date.strftime("%M"))%15==0 and (int(exp_date.timestamp())-int(timestamp))>60*5:
            exp.append(exp_date.timestamp())
            index=index+1
        exp_date= exp_date+timedelta(minutes=1)

    remaning=[]
        
    for idx, t in enumerate(exp):
        if idx>=5:
            dr=15*(idx-4)
        else:
            dr=idx+1
        remaning.append((dr,int(t)-int(time.time())))

    return remaning




 