import platform

def get_monospaced_font():
    font = ""
    os = platform.system()
    if os == "Windows":
        font = "Lucida Console"
    elif os == "MacOS":
        font = "Courier"
    elif os == "Linux":
        font = "DejeVu Sans Mono"

    return font

def get_regular_font():
    font = ""
    os = platform.system()
    if os == "Windows":
        font = "Helvetica"
    elif os == "MacOS":
        font = "San Francisco"
    elif os == "Linux":
        font = "Sans-Serif"

    return font
