import time
import json

import pyotp  # https://github.com/pyauth/pyotp

"""
    TODO list:
    * - [x] Put all values from uri into a JSON file
"""

def get_database():
    """Parse the JSON database for all entries"""
    with open("data.json", "r") as data:
        database = json.load(data)

    return database

def database_append(entry):
    """Append a new entry to the database"""
    with open("data.json", "r") as database:
        current_db = json.load(database) # read all current entries

    current_db.append(entry) # append the new entry

    with open("data.json", "w") as database:
        database.write(json.dumps(current_db, indent = 4)) # write the new database

def parse_uri(uri, parameter):
    """Parse the URI for a parameter

    Deprecated?
    """
    param = ""

    if parameter == "label":
        uri = uri[uri.find("//"):]
        param = uri[uri.find("//")+7 : uri.find(":")]
    elif parameter == "account":
        uri = uri[15:]
        param = uri[uri.find(":") + 1 : uri.find("?")]
    else:
        uri = uri[uri.find(parameter):]
        if parameter == "period":
            param = uri[uri.find(parameter) + len(parameter) + 1 :]
        else:
            param = uri[uri.find(parameter) + len(parameter) + 1 : uri.find("&")]

    param = param.replace('%20', ' ') # remove encoded spaces from URI
    return param

def get_otp(secret):
    """Return OTP from the passed URI"""
    totp = pyotp.TOTP(secret)
    return totp.now()

def get_remaining_time(secret, period = 30):
    """Return remaining time of an OTP code"""
    totp = pyotp.TOTP(secret, interval = float(period))
    time_remaining = (totp.interval - time.time()) % totp.interval
    return time_remaining

if __name__ == "__main__":
    db = get_database()
    for account in db:
        print(account["secret"])
