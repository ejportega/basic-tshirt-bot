# /index.py
from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json

from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    action = get_action(data);
    reply = {}

    if action == 'buy_tshirt_action':
        reply = buy_tshirt_action(data)
        return jsonify(reply)
    elif action == 'buy-tshirt.buy-tshirt-no':
        reply = buy_tshirt_no_action(data)
        return jsonify(reply)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text

def get_action(data):
    req = request.get_json(force=True)
    return req.get('queryResult').get('action')

def get_parameters(data):
    return data['queryResult']['outputContexts'][0]['parameters']

def buy_tshirt_action(data):
    tshirt_size = get_parameters(data)['tshirt_size']
    color = get_parameters(data)['color']
    price = 200.25

    if tshirt_size == 'small':
        price += 150.50
    elif tshirt_size == 'medium':
        price += 220.20
    elif tshirt_size == 'large':
        price += 299.75

    price = price * 2.75;    
    reply = {
        "fulfillmentText": "Great! You ordered color {} and {} size tshirt! The total price is {}. Come pick it up tomorrow in our branch at 1230 Makati City, Metro Manila. Would you like a receipt?".format(color, tshirt_size, price)
    }

    return reply

def buy_tshirt_no_action(data):
    order_id = randint(1000, 10000)
    reply = {
        "fulfillmentText": "Cool no problem. Your Order Id is {}. Thank you for purchasing an item in Basic Tshirt!".format(order_id)
    }

    return reply

# run Flask app
if __name__ == "__main__":
    app.run(debug=True)