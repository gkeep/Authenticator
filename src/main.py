from tkinter import *

import otp

"""
    TODO list:
    * - [ ] Make a GUI
    *    - [ ] Get favicons from websites
    *    - [ ] Optimize for multiple codes
    * - [ ] Add QR code recognition

    FIXME list:
    * - [x] Countdown clock and otp code aren't synchronised
    * - [ ] Place account info and code after each other in column
"""

URIS = {
    "otpauth://totp/ACME%20Co:john@example.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30",
    "otpauth://totp/ACME%20Co:kate@example.com?secret=2ALACOQ5CEW3LWZ5VPELVQNGGQZ5MEWL&issuer=Amazon&algorithm=SHA1&digits=6&period=30",
    "otpauth://totp/ACME%20Co:mike@example.com?secret=KXNEYIS3I5EFCKVSCXIGEV3HUYTYFIWB&issuer=Google&algorithm=SHA1&digits=6&period=30"}

labels = []
info = []

root = Tk()

# label that displays the OTP code
class OTPCode():
    def __init__(self):
        i = 0
        for uri in URIS:
            self.root = root
            labels.append(Label(root, text = "", font = ("Fira Code", 20), pady = 20))
            self.label = labels[i]
            self.label.grid(row = i, column = 1)

            self.update_codes(uri, i)
            i += 1

    # update the code every 30 seconds
    def update_codes(self, uri, i):
        labels[i].configure(text = otp.getOTP(uri))

class accountInfo():
    def __init__(self):
        i = 0
        for uri in URIS:
            self.root = root
            account = otp.parseURI(uri, "account")
            issuer = otp.parseURI(uri, "issuer")
            info.append(Label(root, text = (account + " at " + issuer)))
            self.label = info[i]
            self.label.grid(row = i, column = 0, padx = 20)

            i += 1

# countdown clock
class countdownClock():
    def __init__(self):
        self.root = root
        self.label = Label(root, text = "", font = ("Fira Code", 15))
        self.label.grid(row = 1, column = 3)

        self.update()

    def update(self, i = 30):
        if i > 0:
        # preferred color palette: https://primer.style/css/support/color-system
            if i <= 10:
                self.label.configure(fg = "#d73a49")
            elif i <= 20:
                self.label.configure(fg = "#b08800")
            else:
                self.label.configure(fg = "black")

            self.label.configure(text = i)
            i -= 1
            self.root.after(1000, lambda: self.update(i))
        else:
            i = 0
            for uri in URIS:
                OTPCode().update_codes(uri, i)
                self.update()
                i += 1

def main():
    root.title("Python Authenticator")

    accountInfo()
    OTPCode()
    countdownClock()

    root.mainloop()

if __name__ == '__main__':
    main()
