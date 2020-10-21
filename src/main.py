from tkinter import *

import otp

"""
    TODO list:
    * - [ ] Make a GUI
    *    - [ ] Get favicons from websites
    *    - [ ] Optimize for multiple codes
    * - [ ] Add QR code recognition
    * - [ ] Group codes in groups of 2 or 3

    FIXME list:
    * - [x] Countdown clock and otp code aren't synchronised
    * - [ ] Place account info and code after each other in column
    * - [ ] Codes don't refresh if remaining time is not 30 on launch
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
        j = 1
        for i in range(0, len(URIS)):
            self.root = root
            labels.append(Label(root, text = "", font = ("Fira Code", 30), pady = 10))
            self.label = labels[i]
            self.label.grid(row = j, column = 0)
            j += 2
        self.update_codes()

    # update codes
    def update_codes(self):
        i = 0
        for uri in URIS:
            code = otp.getOTP(uri)
            labels[i].configure(text = code)
            i += 1


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

class CountdownClock():
    def __init__(self, codes):
        self.root = root
        self.label = Label(root, text = "", font = ("Fira Code", 20))
        self.label.grid(row = len(URIS), column = 3, padx = 30)

        remaining_time = otp.getRemainingTime(otp.parseURI(URIS[1], "secret"))
        self.update_clock(codes, remaining_time)

    def update_clock(self, codes, i):
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
            self.root.after(1000, lambda: self.update_clock(codes, i))
        else:
            codes.update_codes()
            self.root.after(10, lambda: self.update_clock(codes, 30))

def main():
    root.title("Python Authenticator")

    AccountInfo()
    codes = OTPCode()
    CountdownClock(codes)

    root.mainloop()

if __name__ == '__main__':
    main()
