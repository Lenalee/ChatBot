from flask import Flask, request, abort
from dotenv import load_dotenv
import os
from chat_bot_logic import answer_message, answer_new_chat
import threading
import time
from text_api_chatting import refresh_token

app = Flask(__name__)

load_dotenv(override=True)

def verify_signature(data):
    received_secret = data.get("secret_key")
    if received_secret != os.getenv("WEBHOOK_SECRET_KEY"):
        print("❌ Invalid secret key received!")
        abort(403)  # Forbidden


@app.route("/user_added_to_chat", methods=["POST"])
def receive_user_added_to_chat():
    data = request.json
    verify_signature(data)
    print("Received user added to chat!")
    if request.method == "POST":
        print("📬 Webhook for user added to chat received!:")
        print("recieved data: ", data)
        print("--------------------------------")
        return "OK", 200
    else:
        print("Received incoming chat for get!")
        return "OK", 200
    

@app.route("/incoming_chat", methods=["POST"])
def receive_incoming_chat():
    data = request.json
    verify_signature(data)
    print("Received incoming event!")
    if request.method == "POST":
        print("📬 Webhook for New Chat received!:")
        print("recieved data: ", data)
        print("--------------------------------")
        answer_new_chat(data)
        #TODO should i take over the chat?
        return "OK", 200
    else:
        print("Received incoming chat for get!")
        return "OK", 200

@app.route("/incoming_event", methods=["POST"])
def receive_incoming_event():
    data = request.json
    verify_signature(data)
    print("Received incoming event!")
    if request.method == "POST":
        print("------------------------------------------")
        print("📬 Webhook for incoming event received!:")
        print(data)
        print("------------------------------------------")
        try:
            answer_message(data)
        except Exception as e:
            print(f"Error sending message: {e}")
            return "Internal server error", 500
        return "OK", 200
    else:
        print("Received incoming event for get!")
        return "OK", 200

@app.route("/chat_deactivated", methods=["POST"])
def receive_chat_deactivated():
    data = request.json
    verify_signature(data)
    if request.method == "POST":
        print("------------------------------------------")
        print("📬 Webhook for chat deactivated received!:")
        print(data)
        print("------------------------------------------")
       # TODO add logic to send statistics if needed?
        return "OK", 200
    else:
        print("Received incoming event for get!")
        return "OK", 200


@app.route("/")
def index():
    return "LiveChat Webhook Receiver is running!"

def token_refresh_task():
    while True:
        # Sleep for 23 hours
        time.sleep(23 * 60 * 60)
        try:
            refresh_token()
            print("Token refreshed successfully")
        except Exception as e:
            print(f"Error refreshing token: {e}")

# Start the token refresh thread when the app starts
token_refresh_thread = threading.Thread(target=token_refresh_task, daemon=True)
token_refresh_thread.start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # Listen on all interfaces so Docker/Render can route traffic in
    app.run(host="0.0.0.0", port=port, debug=True)