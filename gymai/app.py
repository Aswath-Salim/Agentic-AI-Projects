import os
os.environ["CREWAI_TELEMETRY_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

from flask import Flask, render_template, request, jsonify
from agents import intake_response, generate_plans

app = Flask(__name__)

INTRO_MESSAGE = (
    "👋 Hi! I’m your AI Gym Coach.\n\n"
    "I’ll ask you a few questions and then create a personalized "
    "workout, diet, and lifestyle plan for you.\n\n"
    "Let’s start — what’s your main fitness goal?"
)


chat_history = []
user_profile = {}
stage = "intake"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global stage

    if len(chat_history) == 0:
        return jsonify({"reply": INTRO_MESSAGE})

    if stage == "intake":
        ai_reply = intake_response(chat_history, user_profile)

        if "PROFILE_COMPLETE" in str(ai_reply):
            stage = "planning"
            return jsonify({"reply": "✅ Got it! Creating your personalized plan..."})
        else:
            chat_history.append(f"AI: {ai_reply}")
            return jsonify({"reply": ai_reply})

    if stage == "planning":
        plans = generate_plans(chat_history)
        stage = "done"
        return jsonify({"reply": plans})

    return jsonify({"reply": "✅ Your plan is ready!"})

if __name__ == "__main__":
    app.run(debug=True)
