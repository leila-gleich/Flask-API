import logging

from flask import Flask, jsonify, render_template, abort, make_response, request
from state_mmmodule import MusicDatastate
from tm_module import MusicDataCity
from module_eventbrite import EventBriteConcerts
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
import csv

today = date.today()
year = str(today.year)
month = str(today.month)
day = str(today.day)

if len(day) == 1:
    day = "0"+ day

if len(month) == 1:
    month = "0" + month


date = year + "-" + month + "-" + day
todaytime = date + "T01:00:00-07:00"

tendays = datetime.now() + timedelta(days=10)
endday = str(tendays.day)
end = year + "-" + month + "-" + endday
end = end + "T23:59:59-07:00"

tm_events_instance= MusicDatastate("CA", todaytime, end)

tm_events=tm_events_instance.data_dic()

city1 = "los" + "%" + "angeles"
city2 = "san" + "%" + "diego"
city3 = "san" + "%" + "francisco"
la_events_instance= MusicDataCity(city1, todaytime, end)
sd_events_instance= MusicDataCity(city2, todaytime, end)
sf_events_instance= MusicDataCity(city3, todaytime, end)
la_events = la_events_instance.data_dic()
sd_events = sd_events_instance.data_dic()
sf_events = sf_events_instance.data_dic()

def get_end():
    endeb = year + "-" + month + "-" + endday
    endeb = endeb + "T02%3A00%3A00Z"
    return endeb

eb_events_instance=EventBriteConcerts(get_end())
eb_events=eb_events_instance.data_dic()

events = eb_events + tm_events + la_events + sd_events + sf_events

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events', methods=['GET'])
def api():
    return jsonify({'events': events})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
