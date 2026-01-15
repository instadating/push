from flask import Flask, request, jsonify, render_template
from pywebpush import webpush, WebPushException
from pymongo import MongoClient
import json

app = Flask(__name__)

# 🔐 VAPID KEYS (GENERATE ONCE – DO NOT CHANGE)
VAPID_PUBLIC_KEY = "BN6tMU7CgGrHp-BA4UtYTrNs6OxL2kk0P2YHU00dATYPFWtu8MEhufhim-7zcSpKwjVcGl1sLi5g-R6L2E8K9l8"
VAPID_PRIVATE_KEY = "s-JCz2PXWjTqy8Ls5was_bwdRmSJu3SFviTSj6Ndnms"
VAPID_CLAIMS = {
    "sub": "mailto:admin@example.com"
}

# 🗄️ MongoDB
client = MongoClient(
    "mongodb+srv://sardfgafdg_db_user:xtARhRbScHTc8bxh@cluster0.ajih9yx.mongodb.net/"
)
db = client["push_db"]
subs = db["subscriptions"]


@app.route("/")
def index():
    return render_template("index.html", public_key=VAPID_PUBLIC_KEY)


# 🔔 SAVE SUBSCRIPTION
@app.route("/subscribe", methods=["POST"])
def subscribe():
    subscription = request.get_json()

    if not subscription:
        return jsonify({"error": "No subscription"}), 400

    subs.update_one(
        {"endpoint": subscription["endpoint"]},
        {"$set": subscription},
        upsert=True
    )

    return jsonify({"success": True})


# 📢 SEND PUSH TO ALL USERS
@app.route("/send")
def send():
    payload = "Hello! This is a Flask push notification 🚀"

    for sub in subs.find():
        try:
            webpush(
                subscription_info=sub,
                data=payload,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
        except WebPushException as ex:
            print("Push failed:", repr(ex))

    return "Sent!"


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
