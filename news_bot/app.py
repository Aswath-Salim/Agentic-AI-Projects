from flask import Flask, render_template, request, jsonify
from crew_agents import run_newsroom

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_news():
    topic = request.json.get("topic")
    article = run_newsroom(topic)
    return jsonify({"article": article})

if __name__ == "__main__":
    app.run(debug=True)
