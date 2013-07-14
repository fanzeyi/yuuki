#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR:   fanzeyi
# CREATED:  16:55:35 14/07/2013
# MODIFIED: 17:45:10 14/07/2013

import string
import random
from datetime import datetime

from flask import abort
from flask import Flask
from flask import request
from flask import redirect
from flask import make_response
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

class URL(db.Model):
    __tablename__ = "URL"
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(20), unique = True)
    url = db.Column(db.String(5000))
    createTime = db.Column(db.DateTime)
    count = db.Column(db.Integer, default = 0)

    def __init__(self, url, code = None):
        self.url = url
        self.createTime = datetime.now()
        self.count = 0
        if code:
            self.code = code
        else:
            for time in xrange(app.config.get("MAX_RETRY_TIME", 5)):
                code = self.genreate_code()
                old_one = self.get_by_code(code)

                if not old_one:
                    self.code = code
                    break
            else:
                raise RuntimeError

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(code = code).first()

    @staticmethod
    def genreate_code():
        return "".join(random.sample(string.ascii_letters + string.digits, app.config.get("URL_LENGTH", 4)))

@app.route('/create', methods = ["POST"])
def create():
    url = request.form["url"]
    code = request.form.get("code", None)

    if app.config.get("PASSWD", ""):
        passwd = app.config.get("PASSWD")
        usr_passwd = request.form.get("passwd")

        if passwd != usr_passwd:
            return abort(404)

    if code:
        old_one = URL.get_by_code(code)
        if old_one:
            return abort(409)

    try:
        zr_url = URL(url, code)
    except RuntimeError:
        return "Short URL allocate pool is full!", 500

    db.session.add(zr_url)
    db.session.commit()

    
    response = make_response()
    response.headers['Location'] = "http://{host}/{code}".format(host = request.host, code = zr_url.code)
    response.status_code = 201
    
    return response

@app.route('/<string:code>')
def locate(code):
    url = URL.get_by_code(code)
    if not url:
        return abort(404)

    url.count = url.count + 1
    db.session.add(url)
    db.session.commit()

    return redirect(url.url)

@app.route('/<string:code>~')
def details(code):
    url = URL.get_by_code(code)
    if not url:
        return abort(404)

    return str(url.count)

if __name__ == '__main__':
    db.create_all()
    app.run()
