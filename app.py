from flask import Flask, request, jsonify, render_template_string # type: ignore
from flask_cors import CORS # type: ignore
import re
import os

app = Flask(__name__)
CORS(app)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>NetServe Chatbot</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #edf0f3;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .chat-container {
      background: white;
      padding: 20px 30px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0,0,0,0.1);
      width: 500px;
    }
    #chatbox {
      height: 300px;
      overflow-y: auto;
      margin-bottom: 10px;
      border: 1px solid #ccc;
      padding: 10px;
      background: #f9f9f9;
    }
    #userInput {
      width: 80%;
      padding: 10px;
      margin-right: 5px;
    }
    #sendButton {
      padding: 10px;
    }
  </style>
</head>
<body>
  <div class="chat-container">
    <h2>Need Help Instantly?</h2>
    <div id="chatbox"></div>
    <input type="text" id="userInput" placeholder="Ask me anything..." />
    <button onclick="handleChatSend()" id="sendButton">Send</button>
  </div>

  <script>
    function handleChatSend() {
      const input = document.getElementById('userInput');
      const message = input.value.trim();
      if (!message) return;

      const chatbox = document.getElementById('chatbox');
      const userMessage = document.createElement('div');
      userMessage.textContent = 'You: ' + message;
      chatbox.appendChild(userMessage);

      fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      })
      .then(response => response.json())
      .then(data => {
        const botReply = document.createElement('div');
        botReply.textContent = 'Bot: ' + data.reply;
        chatbox.appendChild(botReply);
        chatbox.scrollTop = chatbox.scrollHeight;
      })
      .catch(() => {
        const botReply = document.createElement('div');
        botReply.textContent = 'Bot: Sorry, I couldn\'t reach the server.';
        chatbox.appendChild(botReply);
      });

      input.value = '';
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower().strip()

    responses = {
        r"(hello|hi|hey)": "Hello! How can I assist you today?",
        r"(track.*order|order.*status|where.*order)": "You can track your order using the Order ID in the Track Order section.",
        r"(services|repair|support)": "We offer router repair, firmware updates, setup assistance, and warranty support.",
        r"(contact|email|phone)": "You can reach us at support@netservesolutions.com or call +91-9876543210.",
        r"(location|address|where.*located)": "We are located at 123 Service Lane, New Delhi, India.",
        r"(balance|data.*usage|remaining.*data|how.*much.*left)": "You can check your current balance and data usage in the NetServe App or by logging into your account.",
        r"(new plans|latest plans|recharge options|available plans|plan details)": "We have exciting new plans! Basic ₹499/month, Premium ₹799/month with 1Gbps speed and OTT bundle. Check our website for full details.",
        r"(reset.*password|forgot.*password)": "You can reset your password via the login page. Click on 'Forgot Password' and follow the instructions.",
        r"(slow internet|speed issue|network problem|connection.*slow)": "We're sorry to hear that. Please try restarting your router. If the issue persists, contact support.",
        r"(how to pay|payment methods|bill payment|pay.*bill)": "You can pay your bill online using UPI, credit/debit cards, or net banking via our website or app.",
        r"(outage|down|no internet|disconnected)": "We’re not showing any outages currently. Please check your router or contact support if it continues.",
        r"(cancel.*connection|terminate.*account|stop.*service)": "To cancel your connection, please contact our customer care or visit the NetServe portal.",
        r"(installation|how.*setup|technician visit|router install)": "We provide technician-assisted installation. You can book a visit through our app or helpline.",
        r"(working hours|business hours|timings|open.*time)": "Our support team is available 9 AM to 9 PM, Monday to Saturday.",
    }

    for pattern, reply in responses.items():
        if re.search(pattern, message):
            return jsonify({"reply": reply})

    return jsonify({"reply": "I'm sorry, I didn't understand that. Can you please rephrase?"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
