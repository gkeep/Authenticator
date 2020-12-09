import tkinter as tk

import addition_window
import algorithm
import removal_window
import fonts

DATABASE = []

labels = []
info = []

root = tk.Tk()

MONOSPACED_FONT = fonts.get_monospaced_font()
NORMAL_FONT = fonts.get_regular_font()

class OTPCode_Label():
    """Labels, that display the OTP code for an account"""
    def __init__(self):
        j = 1
        global labels
        labels = []
        for i in range(0, len(DATABASE)):
            self.root = root
            labels.append(
                tk.Label(root, text = "", font = (MONOSPACED_FONT, 30)))
            self.label = labels[i]
            self.label.grid(row = j, column = 0, pady = 5)
            j += 2
        self.update_codes()

    # update codes
    @staticmethod
    def update_codes():
        i = 0
        for account in DATABASE:
            secret = account["secret"]
            code = algorithm.get_otp(secret)
            code = code[ : int(len(code) / 2)] + " " + code[int(len(code) / 2) : len(code)] # group codes by 3
            labels[i].configure(text = code)
            i += 1

        if len(labels) > i:
            for idx in range(i + 1, len(labels)):
                labels[idx].label.destroy()

class AccountInfo_Label():
    """Information about an account above the OTP code"""
    def __init__(self):
        i = 0
        j = 0
        global info
        info = []
        for account in DATABASE:
            self.root = root
            account_name = account["account_name"]
            issuer = account["issuer"]
            info.append(
                tk.Label(root, text = (account_name + " at " + issuer), font = (NORMAL_FONT, 12)))
            self.label = info[i]
            self.label.grid(row = j, column = 0, padx = 10)
            i += 1
            j += 2

        # self.update_info()

    @staticmethod
    def update_info():
        print(len(info), " ", len(DATABASE))
        if len(info) > len(DATABASE):
            for idx in range(len(DATABASE) + 1, len(info)):
                info[idx].label.destroy()

class CountdownClock_Label():
    """Countdown clock, shows remaining time of an OTP code"""
    def __init__(self, otps):
        self.root = root
        self.label = tk.Label(root, text = "", font = (MONOSPACED_FONT, 20))
        self.label.grid(row = 1, column = 3, padx = 20)

        remaining_time = algorithm.get_remaining_time()
        self.update_clock(otps, remaining_time)

    # update all OTP codes
    def update_clock(self, otps, i):
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
            self.root.after(1000, lambda: self.update_clock(otps, i))
        else:
            otps.update_codes()
            self.update_clock(otps, 30)

class Add_Button():
    def __init__(self):
        self.root = root
        self.button = tk.Button(self.root, text = "Add", font = (NORMAL_FONT, 15), command = self.create_dialog)
        self.button.grid(row = 2, column = 3)

    @classmethod
    def create_dialog(cls):
        text = []
        input_boxes = []

        dialog_add = tk.Toplevel(root)

        dialog_add.title("Authenticator - new account")
        dialog_add.geometry("550x200")
        dialog_add.resizable(width = False, height = False)
        frame = tk.Frame(dialog_add, padx = 5, pady = 5)
        frame.place(x = 10, y = 0)
        addition_window.Text_Label(frame, text)
        addition_window.Input_InputBox(frame, input_boxes)
        addition_window.Finish_Button(dialog_add, input_boxes)

        dialog_add.lift() # ensure the window appears above all others

        root.wait_window(dialog_add)
        update_all() # update all codes after the addition

class Remove_Button():
    def __init__(self):
        self.root = root
        self.button = tk.Button(self.root, text = "Remove", font = (NORMAL_FONT, 15), command = self.create_dialog)
        self.button.grid(row = 3, column = 3)

    @classmethod
    def create_dialog(cls):
        dialog_remove = tk.Toplevel(root)

        dialog_remove.title("Authenticator - remove account")
        dialog_remove.geometry("550x200")
        dialog_remove.resizable(width = False, height = False)
        frame = tk.Frame(dialog_remove, padx = 5, pady = 5)
        frame.place(x = 10, y = 0)
        accounts = removal_window.Accounts_ListBox(frame, DATABASE)
        removal_window.Remove_Button(frame, accounts)

        dialog_remove.lift() # ensure the window appears above all others

        root.wait_window(dialog_remove)
        update_all() # update all codes after the removal

def update_all():
    global DATABASE
    DATABASE = algorithm.get_database()
    if DATABASE: # do not try to display everything if database is empty
        codes = OTPCode_Label()
        AccountInfo_Label()
        CountdownClock_Label(codes)
        Remove_Button()
    else:
        label_empty = tk.Label(root, text = "Click 'Add' to add new codes!", font = (NORMAL_FONT, 15))
        label_empty.grid(row = 2, column = 0, pady = 20, padx = 10)
    Add_Button()

def main():
    root.title("Authenticator")
    root.resizable(width = False, height = False)
    update_all()

    root.mainloop()

if __name__ == '__main__':
    main()
