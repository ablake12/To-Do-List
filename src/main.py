import tkinter as tk
from ToDo import ToDoList

if __name__ == "__main__":
    window = tk.Tk()
    app = ToDoList(window)
    window.mainloop()