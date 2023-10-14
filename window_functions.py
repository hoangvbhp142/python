from tkinter import Tk, Label, Button, Entry, Frame, END, Toplevel
from tkinter import ttk
from db_operation import Database


class Window:
    def __init__(self, root, database):
        self.root = root
        self.database = database

        self.root.title("Password Manager")
        self.root.geometry("900x500+40+40")

        (Label(self.root, text="Password Manager", width=20, bg="crimson", fg="white", font=("Time New Roman", 20)
               , padx=10, pady=10, highlightbackground="black", highlightthickness=2)
         .grid(columnspan=4, padx=270, pady=20))

        self.curd_frame = Frame(self.root)
        self.curd_frame.grid()
        self.create_entry_labels()
        self.create_entry_boxes()
        self.create_button()
        self.search_entry = Entry(self.curd_frame, width=19, background="light gray", font=("Time New Roman", 15))
        self.search_entry.grid(row=self.row_no - 1, column=self.col_no - 2)
        self.create_records_tree()

    def create_entry_labels(self):
        self.col_no = self.row_no = 0
        labels_info = ("ID", "Website", "Username", "Password")
        for label in labels_info:
            Label(self.curd_frame, text=label, fg="black", font=("Time New Roman", 15)).grid(
                row=self.row_no, column=self.col_no, padx=5, pady=5)
            self.col_no += 1

    def create_button(self):
        self.row_no += 1
        self.col_no = 0
        buttons_info = (
            ("Save", "crimson", self.seve_button),
            ("Update", "crimson", self.update_button),
            ("Delete", "crimson", self.delete_button),
            ("Copy", "crimson", self.copy_button),
            ("Search", "crimson", self.search_button),
            ("Show", "crimson", self.show_button)
        )
        for button in buttons_info:
            if self.col_no == 4:
                self.row_no += 1
                self.col_no -= 1
            Button(self.curd_frame, text=button[0], bg=button[1], command=button[2]
                   , fg="white", font=("Time New Roman", 15)
                   , width=17).grid(row=self.row_no, column=self.col_no, padx=5, pady=5)
            self.col_no += 1

    def create_entry_boxes(self):
        self.entry_boxes = []
        self.col_no = 0
        self.row_no += 1
        for i in range(4):
            show = ""
            if i == 3:
                show = "*"
            entry_box = Entry(self.curd_frame, width=19, background="light gray", font=("Time New Roman", 15),
                              show=show)
            entry_box.grid(row=self.row_no, column=self.col_no, padx=5, pady=5)
            self.col_no += 1
            self.entry_boxes.append(entry_box)

    # function button
    def seve_button(self):
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()

        data = {"website": website, "username": username, "password": password}
        self.database.create_record(data)
        self.show_button()

    def update_button(self):
        ID = self.entry_boxes[0].get()
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()

        data = {"ID": ID, "website": website, "username": username, "password": password}
        self.database.update_record(data)
        self.show_button()

    def delete_button(self):
        ID = self.entry_boxes[0].get()
        self.database.delete_record(ID)
        self.show_button()

    def show_button(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        password_list = self.database.show_records()
        for record in password_list:
            self.records_tree.insert("", END,
                                     values=(record[0], record[3], record[4], record[5]))

    def create_records_tree(self):
        columns = ("ID", "Website", "Username", "Password")
        self.records_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.records_tree.heading("ID", text="ID")
        self.records_tree.heading("Website", text="Website")
        self.records_tree.heading("Username", text="Username")
        self.records_tree.heading("Password", text="Password")

        self.records_tree["display"] = ("Website", "Username")

        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item = self.records_tree.item(selected_item)
                record = item["values"]
                for entry_box, item in zip(self.entry_boxes, record):
                    entry_box.delete(0, END)
                    entry_box.insert(0, item)

        self.records_tree.bind("<<TreeviewSelect>>", item_selected)

        self.records_tree.grid()

    def search_button(self):
        website = self.search_entry.get()
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        password_list = self.database.search_record(website)
        for record in password_list:
            self.records_tree.insert("", END,
                                     values=(record[0], record[3], record[4], record[5]))

    def copy_button(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.entry_boxes[3].get())
        message = "Copied"
        title = "Copy"
        if self.entry_boxes[3].get() == "":
            message = "Box is empty"
            title = "Error"
        self.show_message(title, message)

    def show_message(self, title_box: str = None, message: str = None):
        TIME_TO_WAIT = 900
        root = Toplevel(self.root)
        background = "green"
        if title_box == "Error":
            background = "red"
        root.geometry("200x50+600+300")
        root.title(title_box)
        Label(root, text=message, background=background,
              font=("Time New Roman", 15), fg="white").pack()
        try:
            root.after(TIME_TO_WAIT, root.destroy)
        except Exception as e:
            print("Error", e)

