import tkinter as tk

import algorithm
import fonts

NORMAL_FONT = fonts.get_regular_font()

class Text_Label():
    def __init__(self, root, text):
        self.root = root
        for i in range(0, 3):
            text.append(
                tk.Label(
                    root,
                    text = "",
                    font = (NORMAL_FONT, 15),
                    pady = 10, padx = 10,
                    justify = "left", anchor = "w"
                )
            )
            self.label = text[i]
            self.label.grid(row = i, column = 0, sticky = "W")

        text[0].configure(text = "Issuer")
        text[1].configure(text = "Account name")
        text[2].configure(text = "Secret Key")

class Input_InputBox():
    def __init__(self, root, input_boxes):
        self.root = root
        for i in range(0, 3):
            input_boxes.append(
                tk.Entry(
                    root,
                    font = (NORMAL_FONT, 15),
                    width = 20,
                    justify = "left")
            )
            self.Entry = input_boxes[i]
            self.Entry.grid(row = i, column = 2, columnspan = 2, padx = 10)

        input_boxes[2].configure(width = 30)

class Finish_Button():
    def __init__(self, root, inputs):
        self.root = root
        self.button = tk.Button(
            root,
            text = "Save",
            font = (NORMAL_FONT, 15),
        self.button.place(relx = 0.5, y = 150, anchor = "n")
            command = lambda: self.finish(inputs)
        )

    def finish(self, inputs):
        """Get inputs from text fields and write them to the database"""
        entry = {
            "issuer": inputs[0].get(),
            "account_name": inputs[1].get(),
            "secret": inputs[2].get()
        }

        algorithm.database_append(entry)

        self.root.destroy() # close the window

if __name__ == "__main__":
    root = tk.Tk()
    text = []
    inputboxes = []

    Text_Label(root, text)
    inputs = Input_InputBox(root, inputboxes)
    Finish_Button(root, inputs)

    root.mainloop()
