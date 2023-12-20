from flask import Flask, render_template, url_for, request
from slack_sdk import WebClient
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from functions import draft_email
import openai




# Load environment variables from .env file kickddddd
load_dotenv()

# Set Slack API credentials
# SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
# SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
# SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]
OPENAI_API_KEY = os.environ["OPENAIAPIKEY"]

openai.api_key = OPENAI_API_KEY




flask_app = Flask(__name__)

#MyPracticeKey = os.environ['MyPracticeKey']

@flask_app.route('/')
@flask_app.route('/home')
def index():
    return render_template("index.html")


# Define the Chatbot route
@flask_app.route("/chatbot", methods=["POST"])
def chatbot():
    #get the message input from the user
    user_input = request.form['message']
    #use the OpenAI API to generate a response
    prompt = f"User: {user_input}\nChatbot: "
    chat_history = []
    response = openai.completions.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        stop=["\nUser: ","\nChatbot: "]

    )

    #extract the response text from the OpenAI API result
    bot_response = response.choices[0].text.strip()



    #Add the user input and bot response to the chat history
    chat_history.append(f"User: {user_input}\nChatbot: {bot_response}" )

    #Render the chatbot template with the response text
    return render_template(
        "chatbot.html",
        user_input=user_input,
        bot_response=bot_response,
    )



#
# @app.route('/about')
# def about():
#     return render_template("about.html")
#
#
# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
#     return "User name: " + name + " - id: " + str(id)

#start the flask app
if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=8000)
