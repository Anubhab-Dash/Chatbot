from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Get your OpenAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json(force=True)
        user_query = req.get("queryResult", {}).get("queryText", "")

        # Call OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query}
            ]
        )
        reply = response.choices[0].message.content.strip()

        return jsonify({"fulfillmentText": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"fulfillmentText": "⚠️ Sorry, something went wrong."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
