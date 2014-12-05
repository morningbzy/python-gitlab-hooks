# coding: utf-8

from flask import Flask, request
from asana import asana
import settings
import json
import re


RE_ASANA_TEXT_ID = re.compile('#(\d+)')
RE_ASANA_URL_ID = re.compile('.*https://app.asana.com/(\d+)/(\d+)/(\d+).*')


def filter_asana_task_id(message):
    task_ids = []

    result = RE_ASANA_TEXT_ID.findall(message)
    if result:
        task_ids += result

    if task_ids is None:
        result = RE_ASANA_URL_ID.findall(message)
        if result:
            task_ids += map(lambda x: x[-1], result)

    print 'Parsing ASANA task IDs from message: %s' % message
    print 'Got: %s' % task_ids
    return map(int, task_ids)


app = Flask(__name__)


@app.route('/asana', methods=['POST'])
def asana_hook():
    if request.method == 'POST':
        print 'Got request:', request.data
        data = json.loads(request.data)

        client = asana.AsanaAPI(settings.ASANA_TOKEN, debug=settings.DEBUG)

        # gitlab hook data format https://gitlab.com/help/web_hooks
        ref = data['ref'].split('/', 2)[-1]

        # Only auto-generate ASANA comment when commit NOT to 'master'
        if 'master' in data['ref']:
            return ''

        commits = data['commits']
        if commits and 'merge' in commits[-1]['message'].lower():
            return ''

        for commit in commits:
            task_ids = filter_asana_task_id(commit['message'])

            for task_id in task_ids:
                message = u'{name} push to repo {repo}/{ref} \n check: {gitlab_url} \n {message}'.format(
                    name=data['user_name'],
                    repo=data['repository']['name'],
                    ref=ref,
                    message=commit['message'],
                    gitlab_url=commit['url'])

                print 'Sending to task(ID: %s, message: %s)...' % (task_id, message),
                try:
                    client.add_story(task_id, message)
                    print 'OK'
                except:
                    print 'ERROR'

        # gitlab does not need feedback
        # but if we don't `return`, flask will raise 500
    return ''


if __name__ == '__main__':
    print 'Server starting...'
    app.run(debug=settings.DEBUG)
