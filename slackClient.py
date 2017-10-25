#coding:UTF-8
import yaml
from slackclient import SlackClient


#defalut value
SLACK_TOKEN = ''
SLACK_USER_ID = ''
#loading credentials overwriting values above
with open("credentials.yaml","r") as stream:
    try:
        credentials = yaml.load(stream)
        globals().update(credentials)
    except yaml.YAMLError as exc:
        print(exc)

sc = SlackClient(SLACK_TOKEN)

print(SLACK_TOKEN)
print(SLACK_USER_ID)

sc.api_call(
  "chat.postEphemeral",
  channel="#zzz-slack-sandbox",
  text="Hello from Python! :tada:",
  user=SLACK_USER_ID
)

lst = sc.api_call(
  "reminders.list",
  channel="#zzz-slack-sandbox",
  token=SLACK_TOKEN
)

filtered = list(filter((lambda x: (x.get('complete_ts') == 0) and x.get('recurring') == False),lst.get('reminders')))


print(filtered)