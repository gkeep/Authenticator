import tkinter as tk

import addition_window
import algorithm, fonts

"""
    TODO list:
    * - [ ] Make a GUI
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

database = algorithm.parse_json()

labels = []
info = []

root = tk.Tk()

monospaced_font = fonts.get_monospaced_font()
normal_font = fonts.get_regular_font()

class OTPCode():
    """Labels, that display the OTP code for an account"""
    def __init__(self):
        j = 1
        for i in range(0, len(database)):
            self.root = root
            labels.append(
                tk.Label(root, text = "", font = (monospaced_font, 30), pady = 5))
            self.label = labels[i]
            self.label.grid(row = j, column = 0)
            j += 2
        self.update_codes()

    # update codes
    def update_codes(self):
        i = 0
        for account in database:
            secret = account["secret"]
            code = algorithm.get_otp(secret)
            code = code[ : int(len(code) / 2)] + " " + code[int(len(code) / 2) : len(code)] # group codes by 3
            labels[i].configure(text = code)
            i += 1

class AccountInfo():
    """Information about an account above the OTP code"""
    def __init__(self):
        i = 0
        j = 0
        for account in database:
            self.root = root
            account_name = account["account_name"]
            issuer = account["issuer"]
            info.append(
                tk.Label(root, text = (account_name + " at " + issuer), font = (normal_font, 12)))
            self.label = info[i]
            self.label.grid(row = j, column = 0, padx = 10)
            i += 1
            j += 2

class CountdownClock():
    """Countdown clock, shows remaining time of an OTP code"""
    def __init__(self, OTPs):
        self.root = root
        self.label = tk.Label(root, text = "", font = (monospaced_font, 20))
        self.label.grid(row = 1, column = 3, padx = 20)

        remaining_time = algorithm.get_remaining_time(database[1]["secret"])
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
        self.Button = tk.Button(self.root, text = "Add", font = (normal_font, 15), command = self.create_dialog)
        self.Button.grid(row = 2, column = 3)

    def create_dialog(self):
        text = []
        input_boxes = []

        global dialog_window
        dialog_window = tk.Toplevel(root)

        dialog_window.title("Authenticator - new code")
        dialog_window.geometry("550x200")
        dialog_window.resizable(width = False, height = False)
        frame = tk.Frame(dialog_window, padx = 5, pady = 5)
        frame.place(x = 10, y = 0)
        addition_window.Text(frame, text)
        addition_window.InputBox(frame, input_boxes)
        addition_window.Finish(dialog_window, input_boxes)

        dialog_window.lift() # ensure the window appears above all others

def update_all():
    codes = OTPCode()
    AccountInfo()
    CountdownClock(codes)
    AddButton()

def main():
    root.title("Authenticator")
    update_all()

    root.mainloop()

if __name__ == '__main__':
    main()
