import os
import requests
from flask import Flask, jsonify, send_from_directory, request

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/api/candles")
def candles():
    key = os.getenv("OTCHARTS_API_KEY")
    if not key:
        return jsonify({"error": "API key not configured"}), 400

    symbol = request.args.get("symbol", "EURUSD_otc")
    allowed = ["EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "BTCUSD_otc", "AUDUSD_otc"]

    if symbol not in allowed:
        return jsonify({"error": "Invalid symbol"}), 400

    try:
        response = requests.get(
    "https://otcharts.com/v1/candles",
    params={
        "venue": "otc",
        "symbol": symbol,

                "tf": 60,
                "limit": 100
            },
            headers={"Authorization": f"Bearer {key}"},
            timeout=20
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as error:
        return jsonify({"error": str(error)}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
