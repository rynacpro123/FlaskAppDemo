from flask import Flask, render_template, url_for, request
from slack_sdk import WebClient
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from functions import draft_email

flask_app = Flask(__name__)



@flask_app.route('/')
@flask_app.route('/home')
def index():
    return render_template("index.html")

#
# @app.route('/about')
# def about():
#     return render_template("about.html")
#
#
# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
#     return "User name: " + name + " - id: " + str(id)

#
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8000)
