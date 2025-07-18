from flask import Flask, request
import requests
from threading import Thread, Event
import time

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

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

