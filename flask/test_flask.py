#!/usr/bin/python
#
#
# Learning Flask framework
#
# Update 9/28
#
# 

from flask import Flask, redirect, url_for, render_template, request, session ,escape
import os

#################################
# Create an instance of the app
################################
app = Flask(__name__)

#
# Root page: use redirect to login page
#
@app.route('/')
def hello():
        return redirect(url_for("login"))


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
    #
    # User 'posted' a message to us
    #
    if request.method == 'POST':
        # Check if the user has logged in with session
        user = request.form['username']
        print " User: %s wants to log in!" % (user)
        print " Current session users are: %s" % (session)
        if user in session:
                #return "Logged in as %s" % escape(session['username'])
                #return "Logged in already"
                return render_template("Amazeriffic.html") # login OK, show the page 
        else:
                print "Not logged in yet, validating..."
                if validate_login(request.form['username'], request.form['password']):
                        session[user] = user # store or remember the session user
                        print " Current session users are: %s" % (session)
                        return render_template("Amazeriffic.html") # login OK, show the page 
                else:
                        return "<h1>Login failed</h1>"

    else:
        return render_template("login.html")


#
# Test js
#
@app.route('/testjs')
def testjs():
    return render_template("test-js.html")

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
	return redirect(url_for("login")) 


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
	print url_for('static', filename = 'test.js')

if __name__ == "__main__":
        
        app.secret_key = os.urandom(24)
        print "Generated a secret key for sessions!"
        app.run(host='0.0.0.0',port=6001,debug=True)

