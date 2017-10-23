# -*- coding: utf-8 -*-
import re
from datetime import datetime


str = "10:00 - 11:00 予定ほげ13:00 - 14:00 予定ぴよ15:00 - 16:00 予定ふが"
p = re.compile("[0-9][0-9]:[0-9][0-9] - [0-9][0-9]:[0-9][0-9]")

now = datetime.now()
time_str = now.strftime("%Y-%m-%d ")

titles = p.split(str)
del titles[0]
times  = re.findall(p, str)
print( titles )
print(times)

parsed_times = []

for idx, val in enumerate(times):
    title = titles[idx]
    start_end = times[idx]
    start, end = start_end.split(" - ")
    start_time = datetime.strptime(time_str + start, "%Y-%m-%d " + "%H:%M")
    end_time = datetime.strptime(time_str + end, "%Y-%m-%d " + "%H:%M")
    print(start_time, end_time, title)
