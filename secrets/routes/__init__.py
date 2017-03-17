from flask import request, redirect, render_template, send_file, after_this_request, jsonify, make_response

import os
import os.path
from binascii import hexlify
from functools import wraps

from secrets.app import app, get_st
from secrets.storage import NoSuchSecret
import secrets.routes.admin


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<name>', methods=['GET'])
def get(name):
    try:
        get_st().get_secret(name)
    except NoSuchSecret:
        return render_template('noname.html', name=name)
    return render_template('name.html', name=name)


@app.route('/<name>', methods=['POST'])
def post(name):
    try:
        get_st().update_message(name, request.form.get('note'), request.files.get('file'))
    except NoSuchSecret:
        return render_template('noname.html', name=name)
    return render_template('success.html', name=name)
