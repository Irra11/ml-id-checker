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
        params = {"id": user_id, "server": zone_id}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        nickname = data.get("nickname") or data.get("name")
        if nickname:
            return jsonify({"status": True, "nickname": nickname})
        return jsonify({"status": False, "message": "User not found"}), 404
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# No app.run() needed for Vercel production
import time

@app.route("/ff", methods=["GET"])
def check_ff_nickname():
    user_id = request.args.get("id")

    if not user_id:
        return jsonify({"status": False}), 400

    try:
        for i in range(3):  # retry 3 times
            res = requests.get(
                "https://api.isan.eu.org/nickname/ff",
                params={"id": user_id},
                timeout=10
            )

            data = res.json()

            nickname = (
                data.get("nickname") or
                data.get("name") or
                (data.get("data") or {}).get("nickname")
            )

            if nickname:
                return jsonify({
                    "status": True,
                    "nickname": nickname
                })

            time.sleep(1)  # wait before retry

        return jsonify({
            "status": False,
            "message": "Nickname not found (retry failed)"
        })

    except:
        return jsonify({"status": False}), 500
