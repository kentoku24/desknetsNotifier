#coding:UTF-8

#libraries needs to be installed
#selenium, pyyaml, slackclient, bs4, lxml
# and phantomjs

# get ChromeDriver from here
# https://sites.google.com/a/chromium.org/chromedriver/downloads

from __future__ import absolute_import, division, print_function

import sys
import json
import re

import datetime
import time

import urllib

from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import json
import yaml
from slackclient import SlackClient

#defalut value
SLACK_TOKEN = ''
SLACK_USER_ID = ''
#loading credentials
with open("credentials.yaml","r") as stream:
    try:
        credentials = yaml.load(stream)
        globals().update(credentials)
    except yaml.YAMLError as exc:
        print(exc)

FORMAT = "%Y-%m-%d %H:%M:%S"

def delete_reminder(reminder_id):
    sc = SlackClient(SLACK_TOKEN)
    return sc.api_call(
        "reminders.delete",
        token=SLACK_TOKEN,
        reminder=reminder_id
    )

def post_reminder(text,time):
    sc = SlackClient(SLACK_TOKEN)
    return sc.api_call(
        "reminders.add",
        token=SLACK_TOKEN,
        text=text,
        time=int(time),
        user=SLACK_USER_ID,
        pretty=1
    )

def parse_schedule(string):
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d ")
    
    p = re.compile("[0-9][0-9]:[0-9][0-9] - [0-9][0-9]:[0-9][0-9]")
    titles = p.split(string)
    day = titles[0]
    del titles[0]
    times  = re.findall(p, string)

    out = []
    for idx, val in enumerate(times):
        title = titles[idx]
        start_end = times[idx]
        start, end = start_end.split(" - ")
        start_time = datetime.datetime.strptime(time_str + start, "%Y-%m-%d " + "%H:%M")
        end_time = datetime.datetime.strptime(time_str + end, "%Y-%m-%d " + "%H:%M")
        print(start_time, end_time, title)

        row = [start_time, end_time, title]
        out.append(row)
    return out


class ScreenshotListener(AbstractEventListener):
    def on_exception(self, exception, driver):
        screenshot_name = "00_exception.png"
        driver.get_screenshot_as_file(screenshot_name)
        print("Screenshot saved as '%s'" % screenshot_name)




################## main starts here ##################################

sc = SlackClient(SLACK_TOKEN)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1024,768')
_driver = webdriver.Chrome(chrome_options=options)
driver = EventFiringWebDriver(_driver, ScreenshotListener())

#_driver = webdriver.PhantomJS()
#driver = EventFiringWebDriver(_driver, ScreenshotListener())

try:
    print( 'drive start' )
    url = "https://www1.j-motto.co.jp/fw/dfw/po80/portal/jsp/J10201.jsp?https://www1.j-motto.co.jp/fw/dfw/gws/cgi-bin/aspioffice/iocjmtgw.cgi?cmd=login"

    driver.get(url)
    driver.implicitly_wait(10)

    memberId_box = driver.find_element_by_id('memberID')
    userId_box = driver.find_element_by_id('userID')
    pass_box = driver.find_element_by_id('password') 
    memberId_box.send_keys(JMOTTO_GROUP)
    userId_box.send_keys(JMOTTO_USERNAME)
    pass_box.send_keys(JMOTTO_PASSWORD)

    driver.save_screenshot('0before login.png')
    print( "saved before login" )

    #login
    driver.find_element_by_name('NAME_DUMMY04').click()

    #elemは特に使わないが、ページが表示されるまで待ちたいため入れている
    elem = driver.find_element_by_css_selector(".portal-cal-body")

    driver.save_screenshot('1after login.png')
    print( "saved after login" )

    soup = BeautifulSoup(driver.page_source, "lxml")

    print("parsing table")
    table = soup.find('table', {'class': 'cal-h-cell'})
    if(table):
        #do normal
        print("it seems like I got a table")
        None
    else:
        print("going for page2 again")
        driver.get("https://gws44.j-motto.co.jp/cgi-bin/JM0344760/dneo.cgi")

except:
     print("Unexpected error:", sys.exc_info()[0])
     raise
finally:
    driver.quit()


rows = table.find_all() #this raises AttributeError: 'NoneType' object has no attribute 'find_all'
lists = []
for row in rows:
    lst = []
    cols = row.find_all(['td','th'])
    cols = [ele.text.strip() for ele in cols]
    lst.append([ele for ele in cols if ele])
    lists.append(lst)

str_for_today = lists[0][0][0]

#text = json.dumps(lists, sort_keys=True, ensure_ascii=False, indent=4)

out = parse_schedule(str_for_today)
#out_text = json.dumps(out, sort_keys=True, ensure_ascii=False, indent=4)

#json.dump(lists, out, indent=4)
#with open('out.json', 'w') as fh:
#  fh.write(text.encode("utf-8"))

#with open('out2.json', 'w') as fh:
#  fh.write(out_text.encode("utf-8"))

current_reminders = sc.api_call(
  "reminders.list",
  token=SLACK_TOKEN
)

#[{u'creator': u'U2AGD5F8V', u'text': u'meeting', u'complete_ts': 0, u'user': u'U2AGD5F8V', u'time': 1509092700, u'recurring': False, u'id': u'Rm7QL555V4'}]
filtered_reminders = list(filter((lambda x: (x.get('complete_ts') == 0) and x.get('recurring') == False),current_reminders.get('reminders')))
print(filtered_reminders)


#make {time:{title:[id, ...]}} dictionary of current reminders
text_id_dic = {}
for reminder in filtered_reminders:
    _time = reminder[u'time']
    _id = reminder[u'id']
    _text = reminder[u'text']

    if _time not in text_id_dic:
        text_id_dic[_time] = {}
    if _text not in text_id_dic[_time]: 
        text_id_dic[_time][_text] = []

    text_id_dic[_time][_text].append(_id)

print("current reminders")
print(text_id_dic)


for schedule_item in out:
    start_time, end_time, title = schedule_item
    print(start_time)
    print(end_time)
    print(title)

    start_minus_5min = start_time - datetime.timedelta(minutes=5)

    unix_starttime = time.mktime( start_minus_5min.timetuple() )

    #todo remove all reminders having same title and time
    if((unix_starttime in text_id_dic) and (title in text_id_dic[unix_starttime]) ):
        for _reminder_id in text_id_dic[unix_starttime][title]:
            print("removing reminder title:", title, "id", _reminder_id)
            delete_response = delete_reminder(_reminder_id)
            print(delete_response)

    print("posting reminder title:", title, " time:", start_minus_5min)
    response = post_reminder(title,unix_starttime)

    sc.api_call(
      "chat.postEphemeral",
      channel="#zzz-slack-sandbox",
      text=title,
      user=SLACK_USER_ID
    )
    
    print(response)