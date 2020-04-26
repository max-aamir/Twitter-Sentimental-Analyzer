import time,datetime


'''d = date(int(dt[-1:-4]),int(dt[4:7]),int(dt[9:11]))
t = time(int(dt[13:15]),int(dt[16:18]),int(dt[19:21]))
#from datetime import *
#dt = "Sun Nov 11 03:19:35 +0000 2018"
#dtt = datetime.combine(d,t)
#print(t.struct_time.tm_hour)
#t = time(tm_hour)
#t = time(t.tm_hour,t.tm_min,t.tm_sec)
#dt = datetime.combine(d,t)
'''

d = datetime.date.today()
t = time.localtime()
t = datetime.time(t.tm_hour,t.tm_min,t.tm_sec)
dt = datetime.datetime.combine(d,t)
print(type(d),type(t))
print(str(dt))
