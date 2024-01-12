from flask import Flask, render_template, url_for, request
import os
from dotenv import find_dotenv, load_dotenv
import openai
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

#https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot


# Load environment variables from .env file forcing .env file variables to override environment variables
load_dotenv(override=True)

#setOpenAI key
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY


#initialize flask app
flask_app = Flask(__name__)


#create initial message list containing system directive

#cranky old man prompt
#messages = [{"role": "system", "content": "you are a very extremly cranky and antagonistic and angry old man that is also a helpful assistant. Your name is Kyle Bybee. You live in Utah but plan to move to Bellingham someday. Your going to be very wealthy someday. You use swear words a lot lot lot lot. "}]

#christian dad prompt
messages = [{"role": "system", "content": "you are a very sweet and approachable assistant that is also a father. You use dad jobkes a lot lot lot. You like to give words of wisdom from the bible.  "}]



#stuff skipped to create local vector database. Perhaps can utilize pinecone instead?
#https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot

retriever = db.as_retriever(
    search_type="similarity", search_kwargs={"k": 2}
)

llm = ChatOpenAI(model_name='gpt-3.5-turbo')
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

@flask_app.route('/')
@flask_app.route('/home')
def index():
    return render_template("index.html")


# Define the Chatbot route
@flask_app.route("/chatbot", methods=["POST"])
def chatbot():

    while True:

        #obtain the message value input by the user in the message form
        user_input = request.form['message']

        #append the human response to our input messages list for future calls to openai
        messages.append({"role": "user", "content": user_input})

        #call openai and pass along message list containing all system, assistance and user inputs within the messages list
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.9,
            top_p=0.6,
            max_tokens=200,
            messages=messages
        )

        #extract the response text from the OpenAI API result
        #bot_response = response.choices[0].text.strip()
        #bot_response = response.choices[0].finish_reason
        bot_response = response.choices[0].message.content




        #append the bot response to our input messages list for future calls to openai
        messages.append({"role": "assistant", "content": bot_response})


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
