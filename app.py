from flask import Flask, request, jsonify
from openai import OpenAI
import os

# Initialize Flask
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return "✅ Webhook is running. Use POST /webhook."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json(force=True)
        print("📥 Incoming JSON:", req)

        user_query = req.get("queryResult", {}).get("queryText", "")
        print("💬 User said:", user_query)

        if not user_query:
            raise ValueError("No 'queryText' found in request.")

        # GPT call (OpenAI ≥ 1.0.0)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_query}
            ]
        )

        reply = completion.choices[0].message.content.strip()
        print("🤖 GPT replied:", reply)

        return jsonify({"fulfillmentText": reply})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"fulfillmentText": f"⚠️ Webhook error: {str(e)}"})

# Start Flask server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
