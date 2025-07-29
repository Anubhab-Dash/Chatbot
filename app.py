from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
openai.api_key = "sk-..."  # Replace this with your actual API key

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    user_query = req['queryResult']['queryText']

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_query}
        ]
    )
    reply = completion.choices[0].message['content']

    return jsonify({"fulfillmentText": reply})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
