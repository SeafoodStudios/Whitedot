from flask import Flask, request
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import json
import time
import base64
import hashlib

app = Flask(__name__)

@app.route("/join/", methods=["POST"])
def join():
    try:
        data = request.get_json()
        public_key = str(data.get('public_key'))
        signup_time = str(int(time.time()) + 86400)

        if not public_key:
            return "Missing public key.", 400

        try:
            with open("to_be_verified.json", "r") as f:
                to_be_verified = json.load(f)
        except FileNotFoundError:
            to_be_verified = {}
        except:
            return "Database error.", 400

        non_encoded_key = public_key
        public_key = public_key.encode('utf-8')
        public_key = base64.b64encode(public_key)
        public_key = public_key.decode('utf-8')

        if public_key in to_be_verified:
            return "This key already exists.", 400

        try:
            serialization.load_pem_public_key(
                non_encoded_key.encode('utf-8'),
                backend=default_backend()
            )
        except:
            return "Invalid key format.", 400

        to_be_verified[public_key] = signup_time

        try:
            with open("to_be_verified.json", "w") as f:
                json.dump(to_be_verified, f, indent=2)
        except:
            return "Database error.", 400

        return "Success, you will be added in 24-48 hours.", 200
    except:
        return "Fatal error.", 400

@app.route('/submit_block', methods=['POST'])
def submit_block():
    try:
        data = request.get_json()
        if not data:
            return "Missing JSON field/s.", 400
        index = data.get("index")
        timestamp = data.get("timestamp")
        previous_hash = data.get("previous_hash")
        nonce = data.get("nonce")
        transaction = data.get("transaction")
        if index is None or not str(index).isdigit():
            return "Invalid index field or missing index field.", 400
        index = str(index)
        if timestamp is None or not str(timestamp).isdigit() or not timestamp:
            return "Invalid timestamp field or missing timestamp field.", 400
        timestamp = str(timestamp)
        if not previous_hash:
            return "Missing previous_hash field.", 400
        previous_hash = str(previous_hash)
        if not nonce:
            return "Missing nonce field.", 400
        nonce = str(nonce)
        if not transaction:
            return "Missing transaction field.", 400
        transaction = str(transaction)
    except:
        return "Field input error.", 400

    block = {
        "index": index,
        "timestamp": timestamp,
        "previous_hash": previous_hash,
        "transaction": transaction,
        "nonce": nonce,
    }
    blockjson = json.dumps(block, sort_keys=True)

    hash_object = hashlib.sha256(blockjson.encode())
    hash_hex = str(hash_object.hexdigest())

    if hash_hex.startswith("00000"):
        # Add to mempool.
        pass
    else:
        return "Proof of Work hash must start with 5 zeros."
