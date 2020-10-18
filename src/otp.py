import pyotp # https://github.com/pyauth/pyotp

"""
    TODO list:
    * - [ ] Put all values from schema into a SQL database
"""

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

    # remove encoded spaces from URI
    param = param.replace("%20", ' ')
    return param


def getOTP(schema):
    totp = pyotp.TOTP(parseSchema(schema, "secret"))
    return totp.now()
