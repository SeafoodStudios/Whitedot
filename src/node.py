import requests
import base64
import hashlib
import random
import json
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

class Whitedot:
    def create_keys(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        priv = key.private_bytes(
            serialization.Encoding.DER,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        )
        pub = key.public_key().public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )
        priv = base64.b64encode(priv).decode()
        pub = base64.b64encode(pub).decode()
        return str(priv), str(pub)
    def join_network(self, public_key):
        url = "https://whitedot.pythonanywhere.com/join/"
        data = {
            "public_key": public_key,
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return "Success: " + response.text
        else:
            return "Error: " + response.text
    def submit_block(self, index, previous_hash, transaction, private_key, public_key):
        url = "https://whitedot.pythonanywhere.com/submit_block"
        nonce = 0
        timestamp = int(time.time())

        private_key_bytes = base64.b64decode(private_key)
        priv_key_obj = serialization.load_der_private_key(private_key_bytes, password=None, backend=default_backend())
        message = f"{index}-{previous_hash}-{transaction}-{timestamp}".encode()
        signature_bytes = priv_key_obj.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        signature = base64.b64encode(signature_bytes).decode()

        while True:
            nonce = nonce + 1
            block = {
            "index": str(index),
            "timestamp": str(int(timestamp)),
            "previous_hash": str(previous_hash),
            "transaction": str(transaction),
            "nonce": str(nonce),
            "signature": str(signature),
            "public_key": str(public_key)
            }
            blockjson = json.dumps(block, sort_keys=True)
            hash_object = hashlib.sha256(blockjson.encode())
            hash_hex = str(hash_object.hexdigest())
            if hash_hex.startswith("00000"):
                break
        data = {
            "index": str(index),
            "timestamp": str(int(timestamp)),
            "previous_hash": str(previous_hash),
            "transaction": str(transaction),
            "nonce": str(nonce),
            "signature": str(signature),
            "public_key": str(public_key)
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return "Success: " + response.text
        else:
            return "Error: " + response.text
    def vote_block(self, vote, index, private_key, public_key):
        url = "https://whitedot.pythonanywhere.com/vote/"
        private_key_bytes = base64.b64decode(private_key)
        private_key = serialization.load_der_private_key(private_key_bytes, password=None, backend=default_backend())
        message = f"{index}-{vote}".encode()
        signature_to_encode = private_key.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        signature = base64.b64encode(signature_to_encode).decode()
        data = {
            "vote": vote,
            "index": index,
            "signature": signature,
            "public_key": public_key
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return "Success: " + response.text
        else:
            return "Error: " + response.text
    def get_blockchain(self):
        response = requests.get("https://whitedot.pythonanywhere.com/blockchain/")
        if response.status_code == 200:
            return response.text
        else:
            return "Error: " + response.text
    def get_mempool(self):
        response = requests.get("https://whitedot.pythonanywhere.com/mempool/")
        if response.status_code == 200:
            return response.text
        else:
            return "Error: " + response.text
    def verify_blockchain(self):
        response = requests.get("https://whitedot.pythonanywhere.com/blockchain/")
        if not response.status_code == 200:
            return "Error: " + response.text
        blockchain = json.loads(str(response.text))

        verified = 1
        for i in range(len(blockchain)):
            block = blockchain[i]
            public_key = block["public_key"]
            signature = block["signature"]
            if i == 0 and block["transaction"] == "Genesis Block" and block["previous_hash"] == "0":
                previous_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
                pass
            else:
                if previous_hash == block["previous_hash"]:
                    pass
                else:
                    verified = 0

                if hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest().startswith("00000"):
                    pass
                else:
                    verified = 0
                message = f"{block['index']}-{block['previous_hash']}-{block['transaction']}-{block['timestamp']}"
                public_key_obj = serialization.load_der_public_key(base64.b64decode(public_key), backend=default_backend())
                try:
                    public_key_obj.verify(
                    base64.b64decode(block["signature"]),
                    message.encode(),
                    padding.PKCS1v15(),
                    hashes.SHA256()
                    )
                except:
                    verified = 0
                previous_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
        if verified == 1:
            return "Blockchain is valid."
        else:
            return "Blockchain is not valid"
