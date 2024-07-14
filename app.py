from flask import Flask, request
import logging
from bot import process_update, main as bot_main

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

updater = bot_main()
dispatcher = updater.dispatcher

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        logging.debug(f"Received update: {update}")
        process_update(update, dispatcher)
        return "OK", 200
    except Exception as e:
        logging.exception("Error processing webhook")
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
