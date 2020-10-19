from tkinter import *

import otp

"""
    TODO list:
    * - [ ] Make a GUI
    * - [ ] Add QR code recognition
"""

SCHEMA = "otpauth://totp/ACME%20Co:john@example.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30"
URI = "otpauth://totp/ACME%20Co:john@example.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30"

root = Tk()

class OTPCode():
    def __init__(self):
        self.root = root
        self.label = Label(root, text = "", font = ("Fira Code", 20))
        self.label.grid(row = 1, column = 0)

        self.update()

    # update the code every 30 seconds
    def update(self):
        self.label.configure(text = otp.getOTP(URI))

# countdown clock
class countdownClock():
    def __init__(self):
        self.root = root
        self.label = Label(root, text = "", font = ("Fira Code", 15))
        self.label.grid(row = 1, column = 1)
        self.update(30)

    def update(self, i):
        if i > 0:
            self.label.configure(text = i)
            i -= 1
            self.root.after(1000, lambda: self.update(i))
        else:
            OTPCode().update()
            self.update(30)

def main():
    root.title("Python TOTP")
    # root.geometry("768x480")

    accountLabel = Label(root, text = otp.parseSchema(SCHEMA, "account"))
    accountLabel = Label(root, text = (otp.parseSchema(URI, "account") + " " + otp.parseSchema(URI, "label")), padx = 20, pady = 5)
    accountLabel.grid(row = 0, column = 0)

    labelLabel = Label(root, text = otp.parseSchema(SCHEMA, "label"))
    OTPCode()

    countdownClock()

    # buttonRefresh = Button(root, text = "Refresh tokens", command=OTPCode)
    # buttonRefresh.grid(row = 1, column = 3)

    root.mainloop()

if __name__ == '__main__':
    main()
