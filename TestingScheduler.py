__author__ = 'henryqin'

from random import uniform
import sched, time
from datetime import datetime
import math
s = sched.scheduler(time.time, time.sleep)
def print_time(): print("From print_time", time.time())


start_time = time.time()
interval_time = 6
while time.time() < start_time + interval_time:
    ramp_range = uniform(1,5)
    s.enter(ramp_range, 1, print, 'Hello')
    s.run()

print(time.strftime("%H:%M:%S"))

timestamp1 = "03:25:32"
timestamp2 = time.strftime("%H:%M:%S")

t1 = datetime.strptime(timestamp1, "%H:%M:%S")
t2 = datetime.strptime(timestamp2, "%H:%M:%S")

difference = t1 > t2

print(difference) # 380, in this case

print(math.sin(5))