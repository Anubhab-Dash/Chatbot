import openai
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json(force=True)
        user_query = req.get("queryResult", {}).get("queryText", "")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_query}
            ]
        )

        reply = completion.choices[0].message.content.strip()
        return jsonify({"fulfillmentText": reply})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"fulfillmentText": f"⚠️ Webhook error: {str(e)}"})
