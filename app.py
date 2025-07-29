from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json(force=True)
        print("📥 Incoming JSON:", req)

        user_query = req.get("queryResult", {}).get("queryText", "")
        print("💬 User said:", user_query)

        if not user_query:
            raise ValueError("No 'queryText' in the request.")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print("🤖 GPT replied:", reply)

        return jsonify({"fulfillmentText": reply})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"fulfillmentText": f"⚠️ Webhook error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
