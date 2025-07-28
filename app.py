from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env file into environment

openai.api_key = os.getenv("OPENAI_API_KEY")  # get key from environment

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    if not user_msg:
        return jsonify({"error": "Missing 'message'."}), 400

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an NPC in a Roblox game."},
                      {"role": "user", "content": user_msg}],
            temperature=0.7
        )
        reply = resp.choices[0].message.content
        return jsonify({"reply": reply})
    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
