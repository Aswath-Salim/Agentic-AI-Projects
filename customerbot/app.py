from flask import Flask, render_template, request, jsonify
from customer_bot import handle_customer_message
import uuid

app = Flask(__name__)

SESSION_ID = str(uuid.uuid4())

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    reply = handle_customer_message(user_msg, SESSION_ID)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
