from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load common passwords into memory
try:
    with open('rockyou.txt', 'r', encoding='utf-8', errors='ignore') as file:
        common_passwords = set(line.strip() for line in file)
except FileNotFoundError:
    raise FileNotFoundError("The file 'rockyou.txt' was not found. Please ensure it is in the same directory as 'server.py'.")

def check_password_strength(password):
    strength = {
        "length": len(password) >= 8,
        "uppercase": any(char.isupper() for char in password),
        "lowercase": any(char.islower() for char in password),
        "numbers": any(char.isdigit() for char in password),
        "special": any(not char.isalnum() for char in password),
    }
    return strength

@app.route('/api/check-password', methods=['POST', 'OPTIONS'])
def check_password():
    if request.method == 'OPTIONS':
        # Respond to CORS preflight request
        return '', 204

    data = request.json
    password = data.get('password', '')

    if not password:
        return jsonify({"error": "Password is required"}), 400

    strength = check_password_strength(password)
    is_common = password in common_passwords

    return jsonify({"strength": strength, "is_common": is_common})

# Health check endpoint for Render
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok"}), 200

# Optional: root endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Password Checker API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)

