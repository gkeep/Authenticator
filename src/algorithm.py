import time
import json
import os

import pyotp  # https://github.com/pyauth/pyotp

def get_database():
    """Parse the JSON database for all entries"""
    file_path = "data.json"
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump("", file) # create empty database if it does not exist

    with open(file_path, "r") as data:
        database = json.load(data)

    return database

def database_append(entry):
    """Append a new entry to the database"""
    with open("data.json", "r") as database:
        current_db = json.load(database) # read all current entries

    current_db.append(entry) # append the new entry

    with open("data.json", "w") as database:
        database.write(json.dumps(current_db, indent = 4)) # write the new database

def database_remove(entry):
    """Remove an entry from the database"""
    with open("data.json", "r") as init_database:
        database = json.load(init_database) # read all current entries

    for account in database:
        if account["account_name"] == entry: # remove the account
            database.remove(account)

    with open("data.json", "w") as finish_database:
        finish_database.write(json.dumps(database, indent = 4)) # write the new database

def get_otp(secret):
    """Return OTP from the passed URI"""
    totp = pyotp.TOTP(secret)
    return totp.now()

def get_remaining_time(period = 30):
    """Return remaining time of an OTP code"""
    totp = pyotp.TOTP("", interval = float(period))
    time_remaining = (totp.interval - time.time()) % totp.interval
    return time_remaining

if __name__ == "__main__":
    db = get_database()
    for account in db:
        print(account["secret"])
