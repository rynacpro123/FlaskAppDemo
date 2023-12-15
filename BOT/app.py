from flask import Flask, render_template, url_for
from slack_sdk import WebClient

flask_app = Flask(__name__)

#kick1

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


# if __name__ == "__main__":
#     flask_app.run()
