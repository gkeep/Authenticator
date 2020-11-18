import tkinter as tk

import otp, add

"""
    TODO list:
    * - [ ] Make a GUI
    *    - [ ] Get favicons from websites
    *    - [x] Optimize for multiple codes
    *    - [ ] Add 'Add' and 'Remove' menus
    *       - [ ] Add by inputing the values
    *       - [ ] Add QR code recognition
    * - [x] Group codes in groups of 2 or 3

    FIXME list:
    * - [x] Countdown clock and otp code aren't synchronised
    * - [x] Place account info and code after each other in column
    * - [x] Codes don't refresh if remaining time is not 30 on launch
"""

URIS = [
    "otpauth://totp/ACME%20Co:john@acme.co?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30",
    "otpauth://totp/ACME%20Co:kate@amazon.co.uk?secret=2ALACOQ5CEW3LWZ5VPELVQNGGQZ5MEWL&issuer=Amazon&algorithm=SHA1&digits=6&period=30",
    "otpauth://totp/ACME%20Co:mike@google.com?secret=KXNEYIS3I5EFCKVSCXIGEV3HUYTYFIWB&issuer=Google&algorithm=SHA1&digits=6&period=30"
]

labels = []
info = []

root = tk.Tk()

class OTPCode():
    """Labels, that display the OTP code for an account"""
    def __init__(self):
        j = 1
        for i in range(0, len(URIS)):
            self.root = root
            labels.append(
                tk.Label(root, text = "", font = ("monospaced", 30), pady = 10))
            self.label = labels[i]
            self.label.grid(row = j, column = 0)
            j += 2
        self.update_codes()

    # update codes
    def update_codes(self):
        i = 0
        for uri in URIS:
            code = algorithm.get_otp(uri)
            code = code[ : int(len(code) / 2)] + " " + code[int(len(code) / 2) : len(code)] # group codes by 3
            labels[i].configure(text = code)
            i += 1

class AccountInfo():
    """Information about an account above the OTP code"""
    def __init__(self):
        i = 0
        j = 0
        for uri in URIS:
            self.root = root
            account = otp.parse_uri(uri, "account")
            issuer = otp.parse_uri(uri, "issuer")
            info.append(
                tk.Label(root, text = (account + " at " + issuer)))
            self.label = info[i]
            self.label.grid(row = j, column = 0, padx = 20)
            i += 1
            j += 2

class CountdownClock():
    """Countdown clock, shows remaining time of an OTP code"""
    def __init__(self, OTPs):
        self.root = root
        self.label = tk.Label(root, text = "", font = ("monospace", 20))
        self.label.grid(row = 1, column = 3, padx = 30)

        remaining_time = otp.get_remaining_time(URIS[1])
        self.update_clock(OTPs, remaining_time)

    # update all OTP codes
    def update_clock(self, OTPs, i):
        if i > 0:
            # preferred color palette: https://primer.style/css/support/color-system
            if i <= 10:
                self.label.configure(fg = "#d73a49")
            elif i <= 20:
                self.label.configure(fg = "#b08800")
            else:
                self.label.configure(fg = "#28a745")

            self.label.configure(text = round(i))
            i -= 1
            self.root.after(1000, lambda: self.update_clock(OTPs, i))
        else:
            OTPs.update_codes()
            self.update_clock(OTPs, 30)

class AddButton():
    def __init__(self):
        self.root = root
        self.Button = tk.Button(self.root, text = "Add", font = ("monospace", 15), command = self.newWindow)
        self.Button.grid(row = 2, column = 3)

    def newWindow(self):
        new_window = tk.Toplevel(root)
        add.MainWindow(new_window)

def main():
    root.title("Authenticator")
    # root.geometry("300x400")

    codes = OTPCode()
    AccountInfo()
    CountdownClock(codes)
    AddButton()

    root.mainloop()

if __name__ == '__main__':
    main()
