import tkinter as tk

import algorithm
import fonts

NORMAL_FONT = fonts.get_regular_font()

class Accounts_ListBox():
    def __init__(self, root, DATABASE):
        self.root = root
        self.listbox = tk.Listbox(self.root, width = 50)
        self.listbox.grid(row = 0, column = 0, padx = 15, pady = 15)
        self.update(DATABASE)

    def update(self, DATABASE):
        self.listbox.delete(0, tk.END) # remove all items
        for account in DATABASE:
            self.listbox.insert(tk.END, account["account_name"])

    def delete(self):
        self.listbox.delete(tk.ACTIVE)

class Remove_Button():
    def __init__(self, root, accounts):
        self.root = root
        self.button = tk.Button(root, text = "Delete",
            font = (NORMAL_FONT, 15),
            command = lambda: self.delete(accounts))
        self.button.grid(row = 0, column = 1, padx = 15, pady = 15)

    def delete(self, accounts):
        entry = accounts.listbox.get(tk.ACTIVE)

        accounts.listbox.delete(entry.index(entry))
        algorithm.database_remove(entry)

        update_database()
        accounts.update(DATABASE)

def update_database():
    global DATABASE
    DATABASE = algorithm.get_database()

if __name__ == "__main__":
    root = tk.Tk()
    # root.geometry("500x250")

    update_database()

    accs = Accounts_ListBox(root, DATABASE)
    Remove_Button(root, accs)

    root.mainloop()