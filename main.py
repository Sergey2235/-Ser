import tkinter as tk

from database import init_database, seed_data
from ui import LoginForm

if __name__ == "__main__":
    init_database()
    seed_data()
    root = tk.Tk()
    LoginForm(root)
    root.mainloop()
