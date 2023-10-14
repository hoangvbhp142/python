from window_functions import *
from db_operation import *

if __name__ == "__main__":
    database = Database()
    database.create_table()
    root = Tk()
    mainWindow = Window(root, database)
    root.mainloop()