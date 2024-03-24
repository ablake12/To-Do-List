import tkinter as tk
import json
import os

class ToDoList:
    def __init__(self, window):
        self.window = window
        self.json_path = "data/list.json"
        self.tasks = {}

        self.entry = tk.Entry(window)
        self.entry.pack(fill=tk.X)

        self.add_button = tk.Button(self.window, text="Add Task", command=self.add_task)
        self.add_button.pack(fill=tk.X)

        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.X)

        if os.path.exists(self.json_path):
            print("Retrieving existing list. Welcome back.")
            self.getExistingList()
        else:
            print("New to do list being created.")
            self.task_status = {}

        self.exitFrame = tk.Frame(window)
        self.exitFrame.pack(fill=tk.X)

        self.save_button = tk.Button(self.exitFrame, text="Save", command=self.save_tasks)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.exitFrame, text="Exit", command=self.window.destroy)
        self.exit_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.exitFrame, text="Delete List", command=lambda: self.delete_checklist_window())
        self.delete_button.pack()

        self.entryError = None

    def add_task(self):
        task_input = self.entry.get()
        if task_input:
            if task_input not in self.tasks:
                if self.entryError is not None:
                    self.entryError.destroy()
                    self.entryError = None
                task_value = tk.IntVar()
                task_frame = tk.Frame(self.frame)
                task_frame.pack()
                checkbox = tk.Checkbutton(task_frame, text=task_input, variable=task_value, onvalue=1, offvalue=0, command=lambda name=task_input, val=task_value: self.mark_task(name, val))
                checkbox.pack(side=tk.LEFT, padx=15)
                delete_button = tk.Button(task_frame, text="Delete", command=lambda: self.delete_confirmation(task_input))
                delete_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                self.tasks[task_input] = (task_value, checkbox, delete_button)
                self.task_status[task_input] = task_value.get()
                self.entry.delete(0, tk.END)
                print(self.tasks)
                print(self.task_status)
            else:
                if self.entryError is not None:
                    self.entryError.destroy()
                self.entryError = tk.Label(self.frame, text = f'Task {task_input} is already in your checklist. Please enter another task.')
                self.entryError.pack()

    def add_existing_tasks(self):
        for task_name in self.task_status:
            task_value = tk.IntVar()
            task_frame = tk.Frame(self.frame)
            task_frame.pack()
            checkbox = tk.Checkbutton(task_frame, text=task_name, variable=task_value, onvalue=1, offvalue=0, command=lambda name=task_name, val=task_value: self.mark_task(name, val))
            if self.task_status[task_name] == 1:
                checkbox.select()
            checkbox.pack(side=tk.LEFT, padx=15)
            delete_button = tk.Button(task_frame, text="Delete", command=lambda: self.delete_confirmation(task_name))
            delete_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.tasks[task_name] = (task_value, checkbox, delete_button)
            self.task_status[task_name] = task_value.get()

    def mark_task(self, task_name, task_val):
        self.task_status[task_name] = task_val.get()
    
    def delete_task(self, task_name, confirm_window):
        checkbox = self.tasks[task_name][1]
        delete_button = self.tasks[task_name][2]
        self.tasks.pop(task_name)
        self.task_status.pop(task_name)
        checkbox.destroy()
        delete_button.destroy()
        confirm_window.destroy()

    def save_tasks(self):
        with open(self.json_path, "w") as out_file:
            json.dump(self.task_status, out_file)
        print("Saved!")
        self.window.destroy()
    def delete_confirmation(self, task_name):
        confirm_window = tk.Toplevel(self.window)
        frame = tk.Frame(confirm_window)
        frame.pack()
        question = tk.Label(frame, text = f'Are you sure you want to delete task "{task_name}"?')
        question.pack()
        answerFrame = tk.Frame(confirm_window)
        answerFrame.pack()
        yes = tk.Button(answerFrame, text="Yes", command=lambda: self.delete_task(task_name, confirm_window))
        yes.pack(side=tk.LEFT)
        no = tk.Button(answerFrame, text="No", command=confirm_window.destroy)
        no.pack()
    def delete_checklist_window(self):
        confirm_window = tk.Toplevel(self.window)
        frame = tk.Frame(confirm_window)
        frame.pack()
        question = tk.Label(frame, text = 'Are you sure you want to delete this checklist?')
        question.pack()
        answerFrame = tk.Frame(confirm_window)
        answerFrame.pack()
        yes = tk.Button(answerFrame, text="Yes", command=lambda: self.delete_checklist(confirm_window))
        yes.pack(side=tk.LEFT)
        no = tk.Button(answerFrame, text="No", command=confirm_window.destroy)
        no.pack()
    def delete_checklist(self, confirm_window):
        os.remove(self.json_path)
        confirm_window.destroy()
        self.window.destroy()
    def getExistingList(self):
        try:
            with open(self.json_path, 'r') as in_file:
                # self.tasks = json.load(in_file)
                self.task_status = json.load(in_file)
            self.add_existing_tasks()
        except json.decoder.JSONDecodeError:# data is showing up as empty
            print("Data does not exist or can not be read. Creating new to do list.")
            self.task_status = {}

if __name__ == "__main__":
    window = tk.Tk()
    app = ToDoList(window)
    window.mainloop()