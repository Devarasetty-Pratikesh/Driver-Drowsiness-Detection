from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    try:
        with open("location.html", "r") as f:
            return f.read()
    except Exception as e:
        return f"Error loading location.html: {e}"

@app.route('/save_location', methods=['POST'])
def save_location():
    data = request.json

    with open("location.txt", "w") as f:
        f.write(f"{data['lat']},{data['lng']}")

    print("Saved:", data)

    return "Saved"

app.run(port=5000)