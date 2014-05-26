from flask import Flask, request
from asana import asana
import settings


ASANA = settings.ASANA
DEBUG = settings.DEBUG


app = Flask(__name__)


@app.route('/asana', methods=['POST'])
def asana_hook():
    if request.method == 'POST':
        client = asana.AsanaAPI(ASANA['token'], debug=DEBUG)

        task = client.get_task()
        client.add_story(task, 'my story')


if __name__ == '__main__':
    app.run(debug=DEBUG)

