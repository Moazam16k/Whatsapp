from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from flask import render_template_string

app = Flask(__name__)
CORS(app)

# Serve the HTML content directly
html_content = """<!DOCTYPE html>
<html>
<head>
    <title>WhatsApp Automation</title>
</head>
<body>
    <h1>WhatsApp Automation</h1>
    
    <h2>Login to WhatsApp</h2>
    <button onclick="login()">Login with QR Code</button>
    <p id="qr"></p>

    <h2>Send a Message</h2>
    <input type="text" id="target" placeholder="Enter Mobile Number">
    <input type="text" id="message" placeholder="Enter Message">
    <button onclick="sendMessage()">Send</button>

    <h2>Send Messages from File</h2>
    <input type="file" id="file">
    <button onclick="sendFile()">Upload & Send</button>

    <script>
        function login() {
            fetch('/login')
                .then(response => response.json())
                .then(data => document.getElementById('qr').innerText = "Scan QR: " + data.qr);
        }

        function sendMessage() {
            let target = document.getElementById("target").value;
            let message = document.getElementById("message").value;
            fetch("/send-message", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({target, message})
            });
        }

        function sendFile() {
            let file = document.getElementById("file").files[0];
            let formData = new FormData();
            formData.append("file", file);
            fetch("/send-from-file", { method: "POST", body: formData });
        }
    </script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(html_content)

@app.route('/login', methods=['GET'])
def login():
    # Simulate QR code response (replace with actual implementation)
    return jsonify({"qr": "123456"})

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    target = data.get('target')
    message = data.get('message')
    # Implement actual WhatsApp sending logic here
    return jsonify({"status": "Message sent to " + target})

@app.route('/send-from-file', methods=['POST'])
def send_from_file():
    file = request.files.get('file')
    if file:
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)
        # Process the file and send messages
        return jsonify({"status": "File received and processed"})
    return jsonify({"error": "No file uploaded"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

