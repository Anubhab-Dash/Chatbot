from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("✅ Webhook hit!")
    req = request.get_json(force=True)
    user_query = req.get("queryResult", {}).get("queryText", "No input received")
    
    return jsonify({
        "fulfillmentText": f"✅ Webhook received your message: {user_query}"
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
