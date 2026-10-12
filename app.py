# app.py

"""Flask backend for PayPal + AI hackathon demo.

- Exposes a chat endpoint that forwards the user prompt to OpenAI's Chat Completion API and returns a product suggestion.
- Creates a PayPal order using the sandbox credentials.
- Captures the order after the user approves payment.
"""

import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
import openai

load_dotenv()

app = Flask(__name__)

# PayPal client setup
client_id = os.getenv("PAYPAL_CLIENT_ID")
client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

if not client_id or not client_secret:
    raise RuntimeError("PayPal sandbox credentials not set in .env")

environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
paypal_client = PayPalHttpClient(environment)

# OpenAI client setup
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OpenAI API key not set in .env")

# Simple system prompt for product recommendation
SYSTEM_PROMPT = (
    "You are a helpful shopping assistant. Given a user's request, suggest a single product with a name, short description, and a price in USD. "
    "Return the answer as a JSON object with fields: name, description, price."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    if not user_msg:
        return jsonify({'error': 'Empty message'}), 400

    # Call OpenAI chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.7
    )
    reply = response.choices[0].message.content.strip()
    # Expect JSON – but keep it simple for demo
    return jsonify({'reply': reply})

@app.route('/api/create-order', methods=['POST'])
def create_order():
    data = request.get_json()
    # Expect amount in USD as string, e.g., "19.99"
    amount = data.get('amount')
    if not amount:
        return jsonify({'error': 'Amount required'}), 400

    request_order = OrdersCreateRequest()
    request_order.prefer('return=representation')
    request_order.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": amount
            }
        }]
    })

    try:
        response = paypal_client.execute(request_order)
        order_id = response.result.id
        return jsonify({'orderID': order_id})
    except IOError as ioe:
        return jsonify({'error': str(ioe)}), 500

@app.route('/api/capture-order', methods=['POST'])
def capture_order():
    data = request.get_json()
    order_id = data.get('orderID')
    if not order_id:
        return jsonify({'error': 'orderID required'}), 400

    capture_request = OrdersCaptureRequest(order_id)
    capture_request.request_body({})
    try:
        response = paypal_client.execute(capture_request)
        status = response.result.status
        return jsonify({'status': status, 'details': response.result})
    except IOError as ioe:
        return jsonify({'error': str(ioe)}), 500

if __name__ == '__main__':
    # Flask's built‑in server is fine for the demo
    app.run(debug=True)
