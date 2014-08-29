#!/usr/bin/python
#
#
# Learning Flask framework
#
# Update 8/28/14
#

from flask import Flask, url_for, render_template, request

#################################
# Create an instance of the app
################################
app = Flask(__name__)

#
# Root page
#
@app.route('/')
def hello():
	return "Hello Flask World!"


#
# login validation 
#
def validate_login(username, password):
    print " User = "+username+" Pass = "+password
    if username == 'lid' and password == 'cloud':
        return True 
    else:
        return False

#
# Login page, use a request object
#
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if validate_login(request.form['username'], request.form['password']):
            return render_template("Amazeriffic.html")
        else:
            return "<h1>Login failed</h1>"

    else:
        return render_template("login.html")



#
#   user page: pass a variable in <> to function
#
@app.route('/user/<username>')
def profile(username):
	return '<h1>' + username + "'s" + " profile" + '</h1>'

#
# This will cause redirection with a trailing /
#
@app.route('/projects/')
def projects():
        return "<h1>Projects</h1>"\
	       "<p>Projects Page, sorry there are no projets here!, Please come back later</p>"


# 
# Use an existing template
#
@app.route('/Amazeriffic/')
def ameri_template():
	return render_template("Amazeriffic.html")


#
# This will NOT cause redirection without a trailing /
#
@app.route('/about')
def about():
	return "<h1>About Page</h1>"


#
# Use url_for to generate URLs
#
with app.test_request_context():
	print url_for('profile', username="John Doe")
	print url_for('login')
	print url_for('about')
	print url_for('about',next='/what',nextnext='whatwhat')

if __name__ == "__main__":
	#app.run(debug = True)
        app.run(host='0.0.0.0',port=6001,debug=True)

