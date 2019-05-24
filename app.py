from functools import wraps
import json
#import os

from flask import Flask, redirect

#from authlib.client import OAuth2Session
#import google.oauth2.credentials
#import googleapiclient.discovery

import google_auth

from cred import secret_key

app = Flask(__name__)
app.secret_key = secret_key

app.register_blueprint(google_auth.app)


def login_req(f):
    @wraps(f)
    def _secured(*args, **kwargs):
        if google_auth.is_logged_in():
            pass
        else:
            #return redirect(url_for('/google/login', next=request.url))
            return redirect("/google/login")
        return f(*args, **kwargs)

    return _secured

@app.route('/')
@login_req
def index():
    
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return 'You are not currently logged in.'

@app.route('/faltu')
@login_req
def faltu():

    return 'You are not currently logged in.'


if __name__ == '__main__':
    app.run(host='localhost', port=8040, debug=True)