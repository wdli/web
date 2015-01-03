#!/usr/bin/python
#
# CS535 Web application
#
# Create Jan 2, 2015
#
#
# Require flask ext: 
#  flask-script
#  flask-bootstrap
#  flask-wtf
#

from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('cs535.html')
'''
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
'''

@app.route('/checkDB')
def checkDB():
    return "<h1>DB not found, please wait...!</h1>"

if __name__ == '__main__':
    manager.run()
