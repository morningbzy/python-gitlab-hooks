# coding: utf-8

from flask import Flask, request
from asana import asana
import settings
import json
import re


RE_ASANA_TEXT_ID = re.compile('.*#(\d+).*')
RE_ASANA_URL_ID = re.compile('.*https://app.asana.com/(\d+)/(\d+)/(\d+).*')


def filter_asana_task_id(message):
    task_id = None

    result = RE_ASANA_TEXT_ID.findall(message)
    if result:
        task_id = result[-1]

    if task_id is None:
        result = RE_ASANA_URL_ID.findall(message)
        if result:
            task_id = result[0][-1]

    return int(task_id)


app = Flask(__name__)


@app.route('/asana', methods=['POST'])
def asana_hook():
    if request.method == 'POST':
        data = json.loads(request.data)

        client = asana.AsanaAPI(settings.ASANA_TOKEN, debug=settings.DEBUG)

        # gitlab hook data format https://gitlab.com/help/web_hooks
        last_commit = data['commits'][-1]
        task_id = filter_asana_task_id(last_commit['message'])

        if task_id:
            message = u'{name} push to repo {repo}/{ref} \n check: {gitlab_url} \n {message}'.format(
                name=data['user_name'],
                repo=data['repository']['name'],
                ref=data['ref'].split('/')[-1],
                message=last_commit['message'],
                gitlab_url=last_commit['url'])

            client.add_story(task_id, message)

        # gitlab does not need feedback
        # but if we dont `return`, flask  will raise 500
        return ''


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)

