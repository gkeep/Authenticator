import pyotp # https://github.com/pyauth/pyotp

"""
    TODO list:
    * - [ ] Put all values from uri into a SQL database
"""

def parseSchema(uri, parameter):
    param = ""

    if parameter == "label":
        uri = uri[uri.find("//"):]
        param = uri[uri.find("//")+7 : uri.find(":")]
    elif parameter == "account":
        uri = uri[15:]
        param = uri[uri.find(":") + 1 : uri.find("?")]
    else:
        uri = uri[uri.find(parameter):]
        param = uri[uri.find(parameter) + len(parameter) + 1 : uri.find("&")]

    # remove encoded spaces from URI
    param = param.replace('%20', ' ')
    return param


def getOTP(uri):
    totp = pyotp.TOTP(parseSchema(uri, "secret"))
    return totp.now()
