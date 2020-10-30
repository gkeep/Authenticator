import pyotp # https://github.com/pyauth/pyotp
import datetime
import math

"""
    TODO list:
    * - [ ] Put all values from uri into a JSON file
"""

def parse_uri(uri, parameter):
    """Parse the URI for a parameter"""
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

    # remove encoded spaces from URI
    param = param.replace('%20', ' ')
    return param


def get_otp(uri):
    """Return OTP from the passed URI"""
    totp = pyotp.TOTP(parse_uri(uri, "secret"))
    return totp.now()


def get_remaining_time(uri, period = 30):
    """Return remaining time of an OTP code"""
    totp = pyotp.TOTP(parse_uri(uri, "secret"), interval = float(period))
    time_remaining = (totp.interval - time.time()) % totp.interval
    return time_remaining
