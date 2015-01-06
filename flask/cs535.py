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
# Use templates: cs535.html, cs535-project2.html
#
# To run: ./cs535.py runserver -h 0.0.0.0 or localhost -p 6001 -r
##################################################################

from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

#
#Create flask app and configuration
#
app = Flask(__name__)
app.config['SECRET_KEY'] = "cs535"

#
# Instantiate manager and bootstrap using the app
#
manager   = Manager(app)
bootstrap = Bootstrap(app)

#
# Submission form class
#
class SubmissionForm(Form):
    student_id = StringField("What's your NPU student ID?", validators=[Required()])
    submit = SubmitField('Submit')
    
#
# Route for '/'
# use cs535.html template
#
@app.route('/')
def index():
    return render_template('cs535.html')
#
# Route for 'checkDB'
# Use cs535_projec2.html template
#
@app.route('/checkDB', methods=['GET','POST'])
def checkDB():
    id = None
    form = SubmissionForm()
    if form.validate_on_submit():
        #
        # if validated, use redirect to handle browser refresh
        #
        #session['student_id'] = form.student_id.data
        id = form.student_id.data
        form.student_id.data = ''
        #return redirect(url_for('checkDB'))

    #
    # If validated, then display the template with a real id
    # If not, then display the template with an empty id
    # and template logic will handle it properly
    #
    #return render_template('cs535_project2.html', form=form, name=session.get('student_id'))
    return render_template('cs535_project2.html', form=form, student_id=id)


#
# Main
#
if __name__ == '__main__':
    manager.run()
