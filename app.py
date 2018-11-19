import random
from flask import Flask
from flask import render_template
from flask import Response
import json

from main import burndown_model
from main import task_status_model
from main import timelog_model

app = Flask(__name__)


def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getTaskStatusData')
def getTaskStatusData():
    ts_data = task_status_model.TaskStatusModel()
    content = {
        "data": ts_data.status_count,
        "color_list": ts_data.get_color_list(ts_data.class_list + ts_data.status_list),
        "legend_list": ts_data.class_list + ts_data.status_list,
        "class": ts_data.class_count,
    }
    content_json = json.dumps(content)
    resp = Response_headers(content_json)
    return resp


@app.route('/getBurndownData')
def getBurndownData():
    bd_data = burndown_model.BurndownModel()
    content = {
        "dates": bd_data.date_list,
        "ideals": bd_data.ideal_list,
        "completions": bd_data.completion_list,
        "loss": bd_data.loss_list
    }
    content_json = json.dumps(content)
    resp = Response_headers(content_json)
    return resp


@app.route('/getTimelineData')
def getTimelineData():
    tl_data = timelog_model.TimelogModel()
    content = {
        'weekdays': tl_data.weekdays,
        'date_range': tl_data.week_date_range,
        'data': tl_data.data_list
    }
    content_json = json.dumps(content)
    resp = Response_headers(content_json)
    return resp


@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(400)
def page_not_found(error):
    content = json.dumps({"error_code": "400"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(410)
def page_not_found(error):
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(500)
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp


if __name__ == '__main__':
    app.run(debug=True)  # threaded=True,
