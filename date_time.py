
import pickle

import time
import datetime

import time 
import datetime 

threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 3)) 

timeStamp = int(time.mktime(threeDayAgo.timetuple())) 

threeDayAgoStr = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")

print(threeDayAgoStr)

nowStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(nowStr)
