from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from gpt4all import GPT4All
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model = GPT4All(model_name=model_name) 

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SECRET_KEY'] = 'zerolife'
app.config['SESSION_PERMANENT'] = False 
Session(app)


def get_chat_session():
    if 'chat_session' not in session:
        session['chat_session'] = model.chat_session()
    return session['chat_session']

def getans(question):
    chat_session = get_chat_session()
    response = model.generate(question)
    bot_reply = ''.join(response)
    return bot_reply

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/ask", methods=['POST'])
def answer():

    data = request.get_json()
    user_message = data.get('message', '')
    
    if user_message:
        bot_reply = getans(user_message)
        return jsonify({'response': bot_reply}), 200
    else:
        return jsonify({'response': 'No message received!'}), 400

if __name__ == "__main__":
    app.run(debug=True)
