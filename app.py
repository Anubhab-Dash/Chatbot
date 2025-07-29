pip install flask openai
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"  # Replace with your actual key

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    user_query = req['queryResult']['queryText']

    # Call OpenAI
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful customer support assistant."},
            {"role": "user", "content": user_query}
        ]
    )
    reply = completion.choices[0].message['content']

    return jsonify({
        "fulfillmentText": reply
    })

if __name__ == '__main__':
    app.run(port=5000)
