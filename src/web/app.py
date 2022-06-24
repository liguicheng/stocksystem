import json
import logging
import re
from logging.handlers import TimedRotatingFileHandler

from flask_cors import *
from flask import Flask, request, render_template, Response,redirect,url_for
from web.front_get_data import get_min_data, get_day_data, get_name
from web.handle_csv import update
import sys

from web.log_record import Logger
from web.login import login_into_db, get_user_name
from web.register import register_into_db

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('register_and_login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('mline.html')

@app.route('/register_into_db', methods=['GET', 'POST'])
def register1():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        res = {}
        code = register_into_db(name, email, password)
        res['code'] = code

        return Response(json.dumps(res), mimetype='application/json')
    else:
        pass
@app.route('/login_into_db', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        res = {}
        code = login_into_db(email, password)
        res['code'] = code
        res['name'] = get_user_name(email)

        return Response(json.dumps(res), mimetype='application/json')
    else:
        pass


@app.route('/kcontent', methods=['GET', 'POST'])
def kcontent():
    return render_template('kcontent.html')

@app.route('/mline', methods=['GET', 'POST'])
def mline():
    return render_template('mline.html')

@app.route('/rank', methods=['GET', 'POST'])
def rank():
    return render_template('rank.html')

@app.route('/min_data/', methods=['GET', 'POST'])
def min_data():
    if request.method == 'POST':
        code = request.form.get('name')
        data_list = get_min_data(code)
        return render_template('mline.html', dict_return = data_list)
    else:
        # 如果当日没有开盘，则展示的是前一个交易日的数据
        res = {}
        code = request.args.get('code')
        data_list = get_min_data(code)
        name = get_name(code)
        res['data'] = data_list
        res['name'] = name
        return Response(json.dumps(res), mimetype='application/json')

@app.route('/day_data/', methods=['GET', 'POST'])
def day_data():
    if request.method == 'POST':
        code = request.form.get('name')
        dict_return = get_day_data(code)
        return render_template('kcontent.html', dict_return = dict_return)
    else:
        res = {}
        code = request.args.get('code')
        data_list = get_day_data(code)
        name = get_name(code)
        res['data'] = data_list
        res['name'] = name
        return Response(json.dumps(res), mimetype='application/json')

@app.route('/update_rank/', methods=['GET', 'POST'])
def update_rank():
    if request.method == 'POST':
        pass
    else:
        # 更新股票排名
        update()
        return Response(json.dumps({"code": "200"}), mimetype='application/json')

# @app.route('/query_mline/', methods=['GET', 'POST'])
# def query_mline():
#     if request.method == 'POST':
#         code = request.form.get('code')
#         # 需要判断输入的是属于上交所还是深交所的，前缀不一样
#         data_list = get_min_data(code)
#         return Response(json.dumps(data_list), mimetype='application/json')
#     else:
#         data_list = get_min_data('600519')
#         return Response(json.dumps(data_list), mimetype='application/json')
#
# @app.route('/query_kcontent/', methods=['GET', 'POST'])
# def query_kcontent():
#     if request.method == 'POST':
#         code = request.form.get('code')
#         # 需要判断输入的是属于上交所还是深交所的，前缀不一样
#
#         data_list = get_day_data(code)
#         return Response(json.dumps(data_list), mimetype='application/json')
#     else:
#         data_list = get_day_data('600519')
#         return Response(json.dumps(data_list), mimetype='application/json')


if __name__ == '__main__':
    logger = logging.getLogger('werkzeug')
    handler = TimedRotatingFileHandler(filename='logs/web.log', when='midnight', backupCount=7, encoding='utf-8')
    logger.addHandler(handler)
    app.run(debug = True)