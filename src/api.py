from flask import Flask, request
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import json
import time
import base64
import hashlib

app = Flask(__name__)

@app.route("/join/", methods=["POST"])
def join():
    try:
        data = request.get_json()
        # Public key should be sent as a base64-encoded string representation of the RSA public key, derived from a DER-encoded format.
        public_key = str(data.get('public_key'))
        # Unix time, you should probably use Python's time.time() function :)
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

        non_encoded_key = base64.b64decode(public_key)

        if public_key in to_be_verified:
            return "This key already exists.", 400

        try:
            public_key_validated = serialization.load_der_public_key(non_encoded_key, backend=default_backend())
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
        timestamp = str(int(time.time()))
        previous_hash = data.get("previous_hash")
        nonce = data.get("nonce")
        transaction = data.get("transaction")
        if index is None or not str(index).isdigit():
            return "Invalid index field or missing index field.", 400
        index = str(index)
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
    try:
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
            try:
                with open("mempool.json", "r") as f:
                    mempool = json.load(f)
            except FileNotFoundError:
                mempool = []
            except:
                return "Mempool database error.", 400

            mempool.append(json.loads(blockjson))
            with open("mempool.json", "w") as f:
                json.dump(mempool, f, indent=2)
            return "Success, request added to mempool to be processed", 200
        else:
            return "Proof of work hash must start with 5 zeros.", 400
    except:
        return "Generic error, could be a verification or database error.", 400
@app.route("/mempool/", methods=["GET"])
def mempool():
    try:
        with open("mempool.json", "r") as f:
            mempool = json.load(f)
        return json.dumps(mempool), 200
    except:
        return "Fatal error.", 400
@app.route("/vote/", methods=["POST"])
def vote():
    try:
        data = request.get_json()
        if not data:
            return "Missing JSON data.", 400
        # vote should be yes/no
        vote = data.get("vote")
        validvote = 0
        if not vote:
            return "The vote field should not be empty.", 400
        else:
            if vote == "yes":
                validvote = 1
            if vote == "no":
                 validvote = 1
            if validvote == 0:
                return "The vote field should be either yes or no.", 400
        vote = str(vote)
        # index should be the index of the block
        index = data.get("index")
        if not index or not index.isdigit():
            return "The index field must be a digit.", 400
        # signature should be the index and vote seperated by a dash signed by the user with their private key and encoded with base64
        signature = data.get("signature")
        # public key should be base64 encoded
        public_key = data.get("public_key")
        if not public_key:
            return "Missing public_key field.", 400
        public_key = str(public_key)
        if not signature:
            return "Missing signature field.", 400
        verifysignature = base64.b64decode(signature)
        public_key_bytes = base64.b64decode(public_key)
        pubkey_obj = serialization.load_der_public_key(public_key_bytes, backend=default_backend())

        pubkey_obj.verify(
            verifysignature,
            f"{index}-{vote}".encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        with open("verified.json", "r") as f:
            verified = json.load(f)
        if not public_key in verified:
            return "Key must be validated first.",400

        try:
            with open("votes.json", "r") as f:
                votes = json.load(f)
        except FileNotFoundError:
            votes = {}
        except:
            return "Database error.", 400
        if index not in votes:
            votes[index] = {"votes": {}}
        if public_key in votes[index]["votes"]:
            return "You have already voted on this block.", 400

        votes[index]["votes"][public_key] = vote

        with open("votes.json", "w") as f:
            json.dump(votes, f, indent=2)

        yes_votes = 0
        for voter in votes[index]["votes"]:
            if votes[index]["votes"][voter] == "yes":
                yes_votes += 1
        vote_count = len(votes[index]["votes"])
        no_votes = vote_count - yes_votes
        vote_state = "0"
        if vote_count > len(verified) / 2:
            if yes_votes > no_votes:
                vote_state = "1"
            elif yes_votes < no_votes:
                vote_state = "0"
            else:
                vote_state = "0"
        try:
            with open("mempool.json", "r") as f:
                mempool = json.load(f)
        except FileNotFoundError:
            mempool = []
        except:
            return "Mempool database error.", 400
        if vote_state == "1":
            votes.pop(index)
            with open("votes.json", "w") as f:
                json.dump(votes, f, indent=2)

            try:
                with open("blockchain.json", "r") as f:
                    blockchain = json.load(f)
            except FileNotFoundError:
                blockchain = []
            except:
                return "Blockchain database error.", 400
            full_block = None
            i = 0
            while i < len(mempool):
                block = mempool[i]
                if block.get("index") == index:
                    full_block = mempool[i]
                    break
                i += 1
            if full_block == None:
                return "Block not found in mempool.", 400
            blockchain.append(full_block)

            i = 0
            while i < len(mempool):
                block = mempool[i]
                if block.get("index") == index:
                    mempool.pop(i)
                    break
                i += 1
            with open("mempool.json", "w") as f:
                json.dump(mempool, f, indent=2)
            with open("blockchain.json", "w") as f:
                json.dump(blockchain, f, indent=2)
        else:
            votes.pop(index)
            with open("votes.json", "w") as f:
                json.dump(votes, f, indent=2)
            i = 0
            while i < len(mempool):
                block = mempool[i]
                if block.get("index") == index:
                    mempool.pop(i)
                    break
                i += 1
            with open("mempool.json", "w") as f:
                json.dump(mempool, f, indent=2)
            return "Success, vote counted.", 200

        return "Success, vote counted.", 200
    except:
        return "Fatal error.", 400
@app.route("/blockchain/", methods=["GET"])
def blockchain():
    try:
        try:
            with open("blockchain.json", "r") as f:
                blockchain = json.load(f)
            return json.dumps(blockchain), 200
        except:
            return "Blockchain database error.", 400
    except:
        return "Fatal error.", 400
