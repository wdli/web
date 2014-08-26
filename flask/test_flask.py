#!/usr/bin/python
#
#
# Learning Flask framework
#
# Update 8/25/14
#

from flask import Flask, url_for

#
# Create an instance of the app
#
app = Flask(__name__)

#
# Root page
#
@app.route('/')
def hello():
	return "Hello Flask World!"

#
# Login page
#
@app.route('/login')
def login():
	return "Login page"


#
# user page
#
@app.route('/user/<username>')
def profile(username):
	return username + "'s" + " profile"

#
# This will cause redirection with a trailing /
#
@app.route('/projects/')
def projects():
        return "<h1>Projects</h1>"\
	       "<p>Projects Page, sorry there are no projets here!, Please come back later</p>"

#
# This will NOT cause redirection without a trailing /
#
@app.route('/about')
def about():
	return "<h1>About Page</h1>"



with app.test_request_context():
	print url_for('profile', username="John Doe")

if __name__ == "__main__":
	#app.run(debug = True)
        app.run(host='0.0.0.0',port=6001,debug=True)

