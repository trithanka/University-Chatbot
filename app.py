from flask import Flask, render_template, request
from chatbot import get_chatbot_response, recommend_questions, load_intents_from_file

app = Flask(__name__)

user_name = None
intents = load_intents_from_file('intents.json')

@app.route("/")
def home():
    global user_name
    if user_name is None:
        greeting_message = "Hi! Welcome to our chatbot. What is your name?"
    else:
        greeting_message = f"Nice to meet you, {user_name}! How can I assist you?"
    return render_template('index.html', greeting_message=greeting_message)
@app.route("/location")
def location():
    return render_template('location.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    global user_name
    user_input = request.form['msg']

    if user_name is None:
        user_name = user_input
        response_text = f"Nice to meet you, {user_name}! How can I assist you?"
        recommended_questions = []
    else:
        response_text, recommended_questions, sentiment = get_chatbot_response(user_input)
        recommended_questions = recommend_questions(user_input, intents)

    return render_template('response.html', response_text=response_text, recommended_questions=recommended_questions)


if __name__ == "__main__":
    app.run()
