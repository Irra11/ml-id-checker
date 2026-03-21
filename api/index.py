from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/ml", methods=["GET"])
def check_ml_nickname():
    user_id = request.args.get("id")
    zone_id = request.args.get("zone")

    if not user_id or not zone_id:
        return jsonify({"status": False, "message": "Missing ID or Zone"}), 400

    try:
        url = "https://api.isan.eu.org/nickname/ml"
        params = {
            "id": user_id,
            "server": zone_id,
            "zone": zone_id
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            return jsonify({"status": False, "message": "External API Error"}), 502
            
        data = response.json()
        nickname = data.get("nickname") or data.get("name") or data.get("userName")

        if nickname:
            return jsonify({
                "status": True,
                "id": user_id,
                "zone": zone_id,
                "nickname": nickname
            })
        else:
            return jsonify({"status": False, "message": "Player not found"}), 404

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# This is required for Vercel
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
