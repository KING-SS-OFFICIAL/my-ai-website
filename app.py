from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Get API key from Render environment
API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return "AI Backend is running 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not API_KEY:
            return jsonify({"reply": "Error: API key missing"})

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            }
        )

        result = response.json()

        # If API returns error
        if "error" in result:
            return jsonify({"reply": "API Error: " + str(result["error"])})

        reply = result["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Server Error: " + str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
