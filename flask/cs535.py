#!/usr/bin/python
#
# CS535 Web application
#
# Create Jan 2, 2015
#
#
# Require flask ext: 
#
#  flask-script
#  flask-bootstrap
#  flask-wtf
#  flask-sqlalchemy
#  flask-migrate
#
# Use templates: cs535.html, cs535-project2.html
#
# To run as a server to listen on port 6002:
#     ./cs535.py runserver -h 0.0.0.0 or localhost -p 6002 -r
# To run in python shell for debugging 
#     python cs535.py shell
# To perform db upgrade:
#    python cs535.py db { init, migrate, upgrade}
# Update for different classes: search for UPDATE. You 'll need to enter
#    the new database name and table name for different class
#
# Note on querying an existing database table, e.g CS535.fall14.db
#   Use sqlacodegen to first look at the table class definition:
#   For example,
"""
wdli@wdli-lenovo:flask:$ sqlacodegen sqlite:///CS535.fall14.db
# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class CS535FALL14(Base):
    __tablename__ = 'CS535_FALL14'

    ID = Column(Integer, primary_key=True)
    TIME = Column(String(128))

"""
# Then make sure that your table definition matches closely to the
# output!
#
##################################################################
import os

from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager
from flask.ext.script import Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand

import logging
import time

#
# Create basic flask app and configuration
#
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "cs535"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'CS535.spring15.test.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'CS535.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join('/home/David.Li/workspace/cs535/NPU/server','CS535.db') # UPDATE

#
# Create database
#
db = SQLAlchemy(app)

#
# Create Table: student login record
#   To match the exiting table: __tablename__, ID, and TIME
#   have to the same as the exiting table scheme
#   This is based on the output from sqlacodegen
#
class LoginRecord(db.Model):
    __tablename__='CS535_Spring15' # UPDATE 
    ID   = db.Column(db.Integer, primary_key=True)
    TIME = db.Column(db.String, unique=True)

    def __repr__(self):
        return "<LoginRecord: user ID %s, login time %s>" % (self.ID, self.TIME)

        
#
# Instantiate manager and bootstrap using the app
#
manager   = Manager(app)
bootstrap = Bootstrap(app)

#
# add a shell context to auto load tables
#
def make_shell_context():
    return dict(app=app, db=db, LoginRecord=LoginRecord)

manager.add_command("shell", Shell(make_context=make_shell_context))

#
# add migrate command
#

migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)

#
# cs535Logger class
#
class cs535Logger(object):
    
    def __init__(self, loggingLevel):
        self._logger_ = logging.getLogger(__name__)
        self._logger_.setLevel(loggingLevel)
        logging.basicConfig(filename="cs535_p2_spring15.log")
        

    def log(self, msg):
        
        logmsg = time.ctime() + ":" + msg
        print logmsg
        self._logger_.info(logmsg)
        self._logger_.debug(logmsg)
        
        
         
#
# start logger
#
global cs535logging
cs535logger = cs535Logger(logging.INFO)
		
#
# Class for submission form
#   This inherits from WTF Form class
#
class SubmissionForm(Form):
    #student_id = StringField("What's your NPU student ID?", validators=[Required()])
    student_id = IntegerField("What's your NPU student ID?", validators=[Required()])
    submit     = SubmitField('Submit')
    
#
# Route for '/'
# use cs535.html template
#
@app.route('/')
def index():
    return render_template('cs535.html')
#
# Route for 'checkDB'
#  This comes from cs535.html template
#  Use cs535_projec2.html template
#  It handles both GET and POST
#
@app.route('/checkDB', methods=['GET','POST'])
def checkDB():
    studentrec = []
    form = SubmissionForm()
    if form.validate_on_submit():
        
        #
        # if validated, use redirect to handle browser refresh
        #  if nothing changed, a refresh will send the old data again
        #
        cs535logger.log("---- New student logging in ----")
        studentrec = LoginRecord.query.filter_by(ID=form.student_id.data).all()

        if not studentrec: #empty list
            #print "Unknown student"
            cs535logger.log("Empty student")
            session['student_login'] = ''
            session['known'] = False
        else:
            #print "Known student"
            #print "Student info: " + str(studentrec[0])
            cs535logger.log("Student found %s" % (str(studentrec[0])))
            session['student_login'] = str(studentrec[0])
            session['known'] = True

        
        session['student_id'] = form.student_id.data
        form.student_id.data = ''
        cs535logger.log("form.student_id.data %s" % (session['student_id']))
        return redirect(url_for('checkDB'))

    #
    # If validated, then display the template with a real id
    # If not, then display the template with an empty id
    # and template logic will handle it properly
    #
    #print "Student ID:" + str(session.get('student_id'))
    cs535logger.log("now render template for Student ID:" + str(session.get('student_id')))
    return render_template('cs535_project2.html', 
                           form= form,
                           student_id=session.get('student_id'), 
                           known = session.get('known'),
                           record=session.get('student_login'))

#
# Main
#
if __name__ == '__main__':
    manager.run()
