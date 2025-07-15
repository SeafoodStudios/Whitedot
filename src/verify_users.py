import json
import time
import base64

try:
    try:
        with open("to_be_verified.json", "r") as f:
            to_be_verified = json.load(f)
    except FileNotFoundError:
        to_be_verified = {}
    except Exception as e:
        print("Error: " + str(e))
    try:
        with open("verified.json", "r") as f:
            verified = json.load(f)
    except FileNotFoundError:
        verified = []
    except Exception as e:
        print("Error: " + str(e))

    count = 0
    for key in list(to_be_verified.keys()):
        value = key.encode('utf-8')
        value = base64.b64decode(value)
        value = value.decode('utf-8')

        if int(to_be_verified[key]) <= int(time.time()):
            if value not in verified:
                count = count + 1
                verified.append(value)
                del to_be_verified[key]
            else:
                del to_be_verified[key]

    with open("verified.json", "w") as f:
        json.dump(verified, f, indent=2)

    with open("to_be_verified.json", "w") as f:
        json.dump(to_be_verified, f, indent=2)

    print(f"""Success, {count} users have been verified!""")
except Exception as e:
    print(f"""Error, {e}""")
