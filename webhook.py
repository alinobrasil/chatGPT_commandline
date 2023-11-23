from flask import Flask, request, jsonify
import json
import stripe
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    # Your Stripe webhook secret
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        # Verify the event by checking the signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']  # Contains the payment intent
            print(payment_intent)
            print("PaymentIntent was successful!")
            # Add your business logic here

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=4242)  # Run on port 4242
