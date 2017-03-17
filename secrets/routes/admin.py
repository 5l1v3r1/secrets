from flask import request, redirect, render_template, make_response, send_file

import os
import os.path
from binascii import hexlify
from functools import wraps
from hashlib import sha256

from secrets.app import app, get_st


def check_admin_auth():
    if 'admin_nonce' not in request.cookies or 'admin_auth' not in request.cookies:
        return False
    nonce = request.cookies['admin_nonce'].encode('ascii')
    m = sha256()
    m.update(nonce)
    m.update(app.config['SUPER_SECRET'].encode('ascii'))
    cookie = hexlify(m.digest())
    return cookie == request.cookies['admin_auth'].encode('ascii')


def with_admin_auth(f):
    @wraps(f)
    def g(*args, **kwargs):
        if check_admin_auth():
            return f(*args, **kwargs)
        else:
            return redirect('/admin/auth')
    return g


@app.route('/admin/auth', methods=['GET', 'POST'])
def admin_auth():
    if request.method == 'GET':
        return (
            redirect('/admin')
            if check_admin_auth()
            else render_template('admin/auth.html')
            )
    if request.form.get('password') != app.config['ADMIN_PASSWORD']:
        return render_template('admin/auth.html', invalid=True)
    nonce = hexlify(os.urandom(16))
    m = sha256()
    m.update(nonce)
    m.update(app.config['SUPER_SECRET'].encode('ascii'))
    cookie = hexlify(m.digest())
    response = make_response(redirect('/admin'))
    response.set_cookie('admin_nonce', nonce)
    response.set_cookie('admin_auth', cookie)
    return response


@app.route('/admin/unauth')
@with_admin_auth
def admin_unauth():
    response = make_response(redirect('/admin'))
    response.set_cookie('admin_nonce', expires=0)
    response.set_cookie('admin_auth', expires=0)
    return response


@app.route('/admin')
@with_admin_auth
def admin_console():
    return render_template('admin/index.html')


@app.route('/admin/secrets', methods=['GET'])
@with_admin_auth
def admin_secrets():
    names = get_st().get_names()
    return render_template('admin/secrets.html', names=names)


@app.route('/admin/secrets', methods=['POST'])
@with_admin_auth
def admin_secrets_post():
    name = request.form['name']
    get_st().create_secret(name)
    return redirect('/admin/secrets/{}'.format(name))


@app.route('/admin/secrets/<name>')
@with_admin_auth
def admin_secret(name):
    messages = get_st().get_messages(name)
    return render_template('admin/secret.html', name=name, messages=messages)


@app.route('/admin/files/<int:mid>')
@with_admin_auth
def admin_file(mid):
    st = get_st()
    return send_file(st.file_path(mid), st.file_name(mid))
