"""
THINGS that are DONE:
    1. homepage complete
    2. can create a new question (or poll)
    3. permalinks done w/ entity ids

THINGS to FIX:
    1. multiple instances of same poll issue in db
    2. update nav links
    
THINGS to DO:
    1. show user created polls
    2. show polls in feed
    3. user can only take a poll once
    4. lot of styling and design (proper HTML/CSS)
    
THINGS to DECIDE:
    1. stats db? (and others too)
    2. poll created by user (how to show? take poll or no?)
"""


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# Import the Flask Framework
from flask import Flask, render_template, request, url_for
from werkzeug.routing import BuildError
from google.appengine.ext import db
import random

app = Flask(__name__)
app.debug = True

# permalink method
def permalink(function):
    def inner(*args, **kwargs):
        endpoint, values = function(*args, **kwargs)
        try:
            return url_for(endpoint, **values)
        except BuildError:
            return
    return inner
    
# database for polls
class Poll(db.Model):
    question = db.TextProperty(required=True)
    choice_a = db.TextProperty(required=True)
    choice_b = db.TextProperty(required=True)
    choice_c = db.TextProperty(required=True)
    choice_d = db.TextProperty(required=True)

# homepage
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

# create new poll
@app.route('/newpoll', methods=['GET'])
def newPoll():
    return render_template("new_poll.html")

# create a permalink for the poll
@permalink
@app.route('/polls', methods=['POST'])
def createLink():
    
    """ 
    this method is creating multiple instaces of a poll
    """
    
    # request all data
    question = request.form['question']
    choice_a = request.form['choice_a']
    choice_b = request.form['choice_b']
    choice_c = request.form['choice_c']
    choice_d = request.form['choice_d']
    
    #put new poll in database
    new_poll = Poll(question=question, choice_a=choice_a, choice_b=choice_b, choice_c=choice_c, choice_d=choice_d)
    new_poll.put()
    
    return render_template("permalink.html", question=question, choice_a=choice_a, choice_b=choice_b, choice_c=choice_c, choice_d=choice_d)

# access a poll
@app.route('/polls/<poll_id>', methods=['GET'])
def showPoll(poll_id):
    poll_id = int(poll_id)
    poll = Poll.get_by_id(poll_id)
    return render_template("permalink.html", 
                           question=poll.question, 
                           choice_a=poll.choice_a, 
                           choice_b=poll.choice_b, 
                           choice_c=poll.choice_c, 
                           choice_d=poll.choice_d)

@app.route('/feed', methods=['GET'])
def feed():
    return render_template("index.html")

@app.route('/<poll_id>/stats', methods=['POST'])
def stats(poll_id):
    
    """
    this method is unfinished b/c need another entity for stats, or answers
    """
    
    poll_id = int(poll_id)
    poll = Poll.get_by_id(poll_id)
    return render_template("stats.html", 
                           choice_a=poll.choice_a, 
                           choice_b=poll.choice_b, 
                           choice_c=poll.choice_c, 
                           choice_d=poll.choice_d)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
