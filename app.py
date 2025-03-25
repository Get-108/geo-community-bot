from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_user_by_token, get_all_users

app = Flask(__name__)
CORS(app)

@app.route("/verify", methods=["GET"])
def verify():
    token = request.args.get("token")
    user = get_user_by_token(token)
    if not user:
        return jsonify({"error": "Invalid token"}), 403

    return jsonify({
        "name": user[2],
        "country": user[3],
        "city": user[4]
    })

@app.route("/all", methods=["GET"])
def all_users():
    return jsonify(get_all_users())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
