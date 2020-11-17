import tkinter as tk

text = []
input_boxes = []

class Labels():
    def __init__(self, root):
        self.root = root
        for i in range(0, 5):
            text.append(
                tk.Label(self.root, text = "", font = ("none", 14), pady = 10, width = 20, anchor="w"))
            self.label = text[i]
            self.label.grid(row = i, column = 0)

        text[0].configure(text = "Secret")
        text[1].configure(text = "Account name")
        text[2].configure(text = "Issuer")
        text[3].configure(text = "Digits")
        text[4].configure(text = "Period")

class InputBox():
    def __init__(self, root):
        self.root = root
        for i in range(0, 5):
            input_boxes.append(
                tk.Entry(self.root, width = 20))
            self.Entry = input_boxes[i]
            self.Entry.grid(row = i, column = 1, columnspan = 2)

class MainWindow():
    def __init__(self, root):
        root.title("Add a new code")
        Labels(root)
        InputBox(root)

        for i in text:
            text[i].destroy()
            input_boxes[i].destroy()