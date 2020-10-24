import pyotp # https://github.com/pyauth/pyotp
import datetime
import math

"""
    TODO list:
    * - [ ] Put all values from uri into a SQL database
"""

def parseURI(uri, parameter):
    """
    Parse the URI for a parameter
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

    # remove encoded spaces from URI
    param = param.replace('%20', ' ')
    return param


def getOTP(uri):
    """
    Return OTP from the passed URI
    """
    totp = pyotp.TOTP(parseURI(uri, "secret"))
    return totp.now()


def getRemainingTime(key, period = 30):
    """
    Return remaining time of an OTP code
    """
    totp = pyotp.TOTP(key, interval = float(period))
    time_remaining = math.floor(totp.interval - datetime.datetime.now().timestamp() % totp.interval)
    return time_remaining