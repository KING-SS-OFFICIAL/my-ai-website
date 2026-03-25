from flask_cors import CORS
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "YOUR_API_KEY"
@app.route("/")
def home():
    return "AI Backend is running 🚀"
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": user_message}]
        }
    )

    reply = response.json()["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
