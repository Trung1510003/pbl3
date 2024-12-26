from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import Lmodel
import Lsearch
import manager


app = Flask(__name__)
app.secret_key = '52Hz-chatbot' 
model = Lmodel.loadModel2()

@app.route("/")
def index():
    log = 0
    if "username" in session: log = 1
    return render_template("index.html", log=log)

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/login")
def login():
    if "username" in session:
        return redirect(url_for('chat'))
    return render_template("login.html")

@app.route("/loginCheck", methods=["POST"])
def loginCheck():
    data = request.get_json()
    username = data.get("username", '')
    password = data.get("password", '')
    user = manager.get_user(username)
    if (password==user.password):
        session['username'] = username
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "not-yet"}), 200

@app.route("/regCheck", methods=["POST"])
def regCheck():
    data = request.get_json()
    email = data.get("email", '')
    username = data.get("username", '')
    password = data.get("password", '')

    print(email, username, password)
    user = manager.get_user(username)
    if user == None:
        manager.add_user(username=username, password=password, email=email)
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "not-yet"}), 200

@app.route("/ask", methods=['POST'])
def ask():
    global model
    data = request.get_json()
    user_message = data.get('message', '')
    web_search = data.get('webSearch','')
    links = []
    
    if user_message:
        print(user_message, web_search)
        if web_search == True:
            links, bot_reply = Lsearch.search_google(user_message)
            context = f'trả lời câu hỏi sau:"{user_message}, dựa vào ngữ cảnh này:"{bot_reply}"'
            # context = f'trả lời câu hỏi sau:"{user_message}, bằng cách truy cập các đường link sau {links}"'
            bot_reply = Lmodel.answer2(model=model, context=context)
        else:
            bot_reply = Lmodel.answer2(model=model, context=user_message)
        response = {
            'response' : bot_reply,
            'links' : links
        }
        return jsonify(response), 200
    else:
        return jsonify({'response': 'No message received!'}), 400

if __name__ == "__main__":
    app.run(debug=True)
