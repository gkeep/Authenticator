# https://github.com/pyauth/pyotp
import pyotp

SCHEMA = "otpauth://totp/ACME%20Co:john@example.com?secret=NYO2G5NPHL556J2HSF4AWOGFOZA3SRDR&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30"


def parseSchema(schema, parameter):
    param = ""

    if parameter == "label":
        schema = schema[schema.find("//"):]
        param = schema[schema.find("//")+7 : schema.find(":")]
    elif parameter == "account":
        schema = schema[15:]
        param = schema[schema.find(":") + 1 : schema.find("?")]
    else:
        schema = schema[schema.find(parameter):]
        param = schema[schema.find(parameter) + len(parameter) + 1 : schema.find("&")]

    return param


def getOTP():
    totp = pyotp.TOTP(parseSchema(SCHEMA, "secret"))
    return totp.now()
