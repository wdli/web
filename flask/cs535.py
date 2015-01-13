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
#  flask-sqlalchemy
#
# Use templates: cs535.html, cs535-project2.html
#
# To run: ./cs535.py runserver -h 0.0.0.0 or localhost -p 6001 -r
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


#
# Create basic flask app and configuration
#
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "cs535"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'CS535.spring15.test.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'CS535.fall14.db')

#
# Create database
#
db = SQLAlchemy(app)

#
# Creat Table: student login record
#
class LoginRecordProject2(db.Model):
    __tablename__="login record"
    id = db.Column(db.String, primary_key=True)
    loginTime = db.Column(db.String, unique=True)

    def __repr__(self):
        return "<LoginRecord: user ID %s, login time %s>" % (self.id, self.loginTime)

        
#
# Instantiate manager and bootstrap using the app
#
manager   = Manager(app)
bootstrap = Bootstrap(app)



#
# add a shell context to auto load tables
#
def make_shell_context():
    return dict(app=app, db=db, LoginRecordProject2=LoginRecordProject2)

manager.add_command("shell", Shell(make_context=make_shell_context))


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

    form = SubmissionForm()
    if form.validate_on_submit():
        #
        # if validated, use redirect to handle browser refresh
        #  if nothing changed, a refresh will send the old data again
        #
        session['student_id'] = form.student_id.data
        return redirect(url_for('checkDB'))

    #
    # If validated, then display the template with a real id
    # If not, then display the template with an empty id
    # and template logic will handle it properly
    #
    print "Student ID:" + str(session.get('student_id'))
    return render_template('cs535_project2.html', form=form, student_id=session.get('student_id'))

#
# Main
#
if __name__ == '__main__':
    manager.run()
