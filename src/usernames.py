from flask import Flask, request
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
import os
import json

app = Flask(__name__)

@app.route('/create/', methods=['POST'])
def create():
    # Retrieve data, username has to be alphabetical and public_key has to be base64 DER :)
    try:
        data = request.get_json()
        username = str(data.get("username"))
        public_key = str(data.get("public_key"))
    except:
        # Be angry if they don't give the correct format
        return "Invalid input/s", 400

    # Validate the stuff
    try:
        der_bytes = base64.b64decode(public_key)
        test_public_key = serialization.load_der_public_key(der_bytes, backend=default_backend())
    except:
        return "Invalid key format.", 400
    if not username.isalpha():
        return "Username must be alphabetical only.", 400

    # Start writing the stuff
    if os.path.exists("db.json"):
        with open("db.json", "r") as db:
            py_db_dict = json.load(db)
    else:
        py_db_dict = {}
    if username in py_db_dict:
        return "Item already in list.", 400
    py_db_dict[username] = public_key
    to_be_written = json.dumps(py_db_dict)
    with open("db.json", "w") as db:
        db.write(str(to_be_written))

    # Give response
    return "Success, added to list!", 200

@app.route('/username/<path:subpath>', methods=['GET'])
def username(subpath):
    # Check if the file exists and load it
    if os.path.exists("db.json"):
        with open("db.json", "r") as db:
            py_db_dict = json.load(db)
    else:
        return "There are no usernames in the list.", 400

    # Check if the username exists and returns it
    if str(subpath) in py_db_dict:
        return py_db_dict[str(subpath)], 200
    else:
        return "This username does not exist.", 400
