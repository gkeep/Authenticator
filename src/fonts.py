import platform


def get_monospaced_font() -> str:
    font = ""
    os = platform.system()

    if os == "Windows":
        font = "Lucida Console"
    elif os == "MacOS":
        font = "Courier"
    elif os == "Linux":
        font = "Monospace"

    return font


def get_regular_font() -> str:
    font = ""
    os = platform.system()

    if os == "Windows":
        font = "Arial"
    elif os == "MacOS":
        font = "San Francisco"
    elif os == "Linux":
        font = "Sans-Serif"

    return font
