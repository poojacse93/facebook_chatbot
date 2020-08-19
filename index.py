import credentials
import requests
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/webhook', methods=['GET'])
def webhook_authoriztion():
    verify_token = request.args.get("hub.verify_token")

    if verify_token == credentials.WEBHOOK_VERIFY_TOKEN:
        return request.args.get("hub.challenge")

    return "unable to authorize"

@app.route("/webhook", methods=["POST"])
def webhook_handle():
    data=request.get_json()
    message = data['entry'][0]['msssaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:
        request_body = {
            'recepient' : {
                'id': sender_id
            },
            'message': {"text":"hello, world!"}

        }
        response = request.post('https://graph.facebook.com/v5.0/me/messages?access_token='+credentials.TOKEN,json=request_body).json()
        return response
    return 'ok'

if __name__ == "__main__":
    app.run(threaded=True, port=5000)