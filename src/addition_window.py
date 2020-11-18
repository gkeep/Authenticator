import tkinter as tk
import algorithm, fonts

normal_font = fonts.get_regular_font()

class Text():
    def __init__(self, root, text):
        self.root = root
        for i in range(0, 3):
            text.append(
                tk.Label(root, text = "", font = (normal_font, 15), pady = 10, padx = 10, justify = "left", anchor = "w"))
            self.label = text[i]
            self.label.grid(row = i, column = 0, sticky = "W")

        text[0].configure(text = "Issuer")
        text[1].configure(text = "Account name")
        text[2].configure(text = "Secret")

class InputBox():
    def __init__(self, root, input_boxes):
        self.root = root
        for i in range(0, 3):
            input_boxes.append(
                tk.Entry(root, width = 20, font = (normal_font, 15), justify = "left"))
            self.Entry = input_boxes[i]
            self.Entry.grid(row = i, column = 2, columnspan = 2, padx = 10)

        input_boxes[2].configure(width = 30)

class Finish():
    def __init__(self, root):
        self.root = root
        self.Button = tk.Button(root, text = "Save", font = (normal_font, 15), command = self.quit)
        # self.Button.grid(row = 10, column = 1, rowspan = 3)
        self.Button.place(relx = 0.5, y = 150, anchor = "n")

    def quit(self):
        self.root.destroy()
