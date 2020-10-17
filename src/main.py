import otp
from tkinter import *

"""
    TODO list:
    * - [ ] Finish GUI
    * - [ ] Add QR code recognition

"""

root = Tk()

# root.configure(bg="#161821")

def Click():
    newLabel = Label(root, text = otp.getOTP())
    newLabel.grid(row=5, column=0)

root.title("an awesome project")
root.geometry("768x480")

newButton = Button(root, text="button", command=Click, fg="#c6c8d1", bg="#161821")
newButton.grid(row=0, column=0)

root.mainloop()
