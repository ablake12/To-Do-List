import tkinter as tk
import json
import os
from datetime import datetime

class ToDoList:
    def __init__(self, window):
        self.window = window
        self.window.title("To Do List")
        self.json_path = os.path.join(os.getcwd(), "data", "list.json")
        self.tasks = {}

        self.entry = tk.Entry(window)
        self.entry.pack(fill=tk.X, pady=5)

        self.add_button = tk.Button(self.window, text="Add Task", highlightbackground= "cornflower blue", command=self.add_task)
        self.add_button.pack(fill=tk.X)

        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.X)

        if os.path.exists(self.json_path):
            print("Retrieving existing list. Welcome back.")
            self.get_existing_list()
        else:
            print("New to do list being created.")
            self.task_status = {}

        self.exit_frame = tk.Frame(window)
        self.exit_frame.pack(fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(self.exit_frame, text="Save", activeforeground= "blue", command=self.save_tasks)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.exit_frame, text="Exit", activeforeground= "blue", command=self.window.destroy)
        self.exit_button.pack(side=tk.LEFT, padx=10)

        self.generate_button = tk.Button(self.exit_frame, text="Export List", activeforeground= "blue", command=self.get_file_name)
        self.generate_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.exit_frame, text="Delete List", activeforeground= "blue", command=lambda: self.delete_checklist_window())
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.entryError = None

        self.window.after(100, self.due_date_alert)

    def add_task(self):
        try:
            task_input = self.entry.get()
            if task_input:
                if task_input not in self.tasks: # if task doesn't exist it can be created
                    if self.entryError is not None:
                        self.entryError.destroy()
                        self.entryError = None
                    task_value = tk.IntVar()
                    task_frame = tk.Frame(self.frame)
                    task_frame.pack()
                    checkbox = tk.Checkbutton(task_frame, text=task_input, variable=task_value, onvalue=1, offvalue=0, command=lambda name=task_input, val=task_value: self.mark_task(name, val))
                    checkbox.pack(side=tk.LEFT, padx=15)
                    delete_button = tk.Button(task_frame, text="Delete Task", activeforeground= "blue", command=lambda name=task_input: self.delete_confirmation(name))
                    delete_button.pack(side=tk.RIGHT, fill=tk.X)
                    due_date_entry = tk.Entry(task_frame)  # New entry for due dates
                    due_date_entry.pack(fill=tk.X, side=tk.LEFT)
                    add_date_button = tk.Button(task_frame, text="Add Due Date", activeforeground= "blue", command=lambda name=task_input, frame = task_frame: self.add_due_date(name, frame))
                    add_date_button.pack(fill=tk.X, side=tk.LEFT, expand=True)
                    self.tasks[task_input] = [task_frame, checkbox, delete_button, add_date_button, due_date_entry]
                    self.task_status[task_input] = [task_value.get()]
                    self.entry.delete(0, tk.END)
                else: # if task exist then it can't be added
                    if self.entryError is not None:
                        self.entryError.destroy()
                    self.entryError = tk.Label(self.frame, text = f'Task {task_input} is already in your checklist. Please enter another task.')
                    self.entryError.pack()
        except Exception as error:
            print(f"Error adding new task. Error was: {error}")
    def add_existing_tasks(self):
        try:
            for task_name in self.task_status:
                task_value = tk.IntVar()
                task_frame = tk.Frame(self.frame)
                task_frame.pack()
                checkbox = tk.Checkbutton(task_frame, text=task_name, variable=task_value, onvalue=1, offvalue=0, command=lambda name=task_name, val=task_value: self.mark_task(name, val))
                if self.task_status[task_name][0] == 1: # have the box already checked
                    checkbox.select()
                checkbox.pack(side=tk.LEFT, padx=15)
                delete_button = tk.Button(task_frame, text="Delete Task", activeforeground= "blue", command=lambda name=task_name: self.delete_confirmation(name))
                delete_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                if len(self.task_status[task_name]) > 1: # if task already has a due date 
                    current_due_date = tk.Label(task_frame, text = f'Due Date: {self.task_status[task_name][1]}')
                    current_due_date.pack(fill=tk.X, side=tk.LEFT)
                    due_date_entry = tk.Entry(task_frame)
                    due_date_entry.pack(fill=tk.X, side=tk.LEFT)
                    update_date_button = tk.Button(task_frame, text="Update Due Date", activeforeground= "blue", command=lambda name=task_name, frame = task_frame: self.add_due_date(name, frame))
                    update_date_button.pack(fill=tk.X, side=tk.LEFT, expand=True)
                    self.tasks[task_name] = [task_frame, checkbox, delete_button, update_date_button, due_date_entry, current_due_date]
                    self.task_status[task_name] = [task_value.get(), self.task_status[task_name][1]]
                else: # Adding a due date
                    due_date_entry = tk.Entry(task_frame)
                    due_date_entry.pack(fill=tk.X, side=tk.LEFT)
                    add_date_button = tk.Button(task_frame, text="Add Due Date", activeforeground= "blue", command=lambda name=task_name, frame = task_frame: self.add_due_date(name, frame))
                    add_date_button.pack(fill=tk.X, side=tk.LEFT, expand=True)
                    self.tasks[task_name] = [task_frame, checkbox, delete_button, add_date_button, due_date_entry]
                    self.task_status[task_name] = [task_value.get()]
        except Exception as error:
            print(f"Error uploading existing tasks. Error was: {error}")

    def mark_task(self, task_name, task_val): #get updated tasks
        try:
            self.task_status[task_name][0] = task_val.get()
        except Exception as error:
            print(f"Error marking task. Error was: {error}")
    
    def add_due_date(self, task_name, task_frame):
        try:
            due_date_entry = self.tasks[task_name][4]
            due_date = due_date_entry.get()
            due_date = due_date.strip()# get rid of white spaces
            datetime.strptime(due_date, "%m/%d/%Y")# make sure it's entered in the correct format
            self.tasks[task_name][3].destroy()
            self.tasks[task_name][4].destroy()
            if len(self.task_status[task_name]) > 1: # if due date is just being updated
                self.tasks[task_name][5].destroy()
                current_due_date = tk.Label(task_frame, text = f'Due Date: {due_date}')
                current_due_date.pack(fill=tk.X, side=tk.LEFT)
                due_date_entry = tk.Entry(task_frame)
                due_date_entry.pack(fill=tk.X, side=tk.LEFT)
                update_date_button = tk.Button(task_frame, text="Update Due Date", activeforeground= "blue", command=lambda name=task_name, frame = task_frame: self.add_due_date(name, frame))
                update_date_button.pack(fill=tk.X, side=tk.LEFT, expand=True)
                self.tasks[task_name][3] = update_date_button # update the button being used
                self.tasks[task_name][4] = due_date_entry # update the text box
                self.tasks[task_name][5] = current_due_date # update the due date
                self.task_status[task_name][1] = due_date
            else: # if due date is being added for the first time
                self.task_status[task_name].append(due_date)
                current_due_date = tk.Label(task_frame, text = f'Due Date: {due_date}')
                self.tasks[task_name].append(current_due_date)
                current_due_date.pack(fill=tk.X, side=tk.LEFT)
                due_date_entry = tk.Entry(task_frame)
                due_date_entry.pack(fill=tk.X, side=tk.LEFT)
                update_date_button = tk.Button(task_frame, text="Update Due Date", activeforeground= "blue", command=lambda name=task_name, frame = task_frame: self.add_due_date(name, frame))
                update_date_button.pack(fill=tk.X, side=tk.LEFT, expand=True)
                self.tasks[task_name][3] = update_date_button # update the add button to an update button
                self.tasks[task_name][4] = due_date_entry # update the due date text box
        except ValueError:
            self.due_date_error()
            
    def due_date_error(self): # window to display date error
        try:
            error_window = tk.Toplevel(self.window)
            frame = tk.Frame(error_window)
            frame.pack()
            error_msg = tk.Label(frame, text = 'Please enter a valid date in mm/dd/yyyy format')
            error_msg.pack()
            ok_frame = tk.Frame(error_window)
            ok_frame.pack()
            ok = tk.Button(ok_frame, text="Ok", command=error_window.destroy)
            ok.pack(side=tk.BOTTOM)
        except Exception as error:
            print(f"Error displaying error window. Error was: {error}")

    def delete_task(self, task_name, confirm_window):
        task_frame = self.tasks[task_name][0] # delete frame for the task which will delete all the associate buttons and labels
        task_frame.destroy()
        self.tasks.pop(task_name) #delete task from list
        self.task_status.pop(task_name) #delete task status
        confirm_window.destroy()

    def save_tasks(self):
        try:
            with open(self.json_path, "w") as out_file:
                json.dump(self.task_status, out_file)
            print("Saved!")
            self.window.destroy()
        except Exception as error:
            print(f"Error saving recent task changes. Error was: {error}")
    def delete_confirmation(self, task_name):
        try:
            confirm_window = tk.Toplevel(self.window)
            frame = tk.Frame(confirm_window)
            frame.pack()
            question = tk.Label(frame, text = f'Are you sure you want to delete task "{task_name}"?')
            question.pack()
            answerFrame = tk.Frame(confirm_window)
            answerFrame.pack()
            yes = tk.Button(answerFrame, text="Yes", activeforeground= "blue", command=lambda: self.delete_task(task_name, confirm_window))
            yes.pack(side=tk.LEFT)
            no = tk.Button(answerFrame, text="No", activeforeground= "blue", command=confirm_window.destroy)
            no.pack()
        except Exception as error:
            print(f"Error deleting {task_name} task.")
    def delete_checklist_window(self):
        try:
            confirm_window = tk.Toplevel(self.window)
            frame = tk.Frame(confirm_window)
            frame.pack()
            question = tk.Label(frame, text = 'Are you sure you want to delete this checklist?')
            question.pack()
            answerFrame = tk.Frame(confirm_window)
            answerFrame.pack()
            yes = tk.Button(answerFrame, text="Yes", activeforeground= "blue", command=lambda: self.delete_checklist(confirm_window))
            yes.pack(side=tk.LEFT)
            no = tk.Button(answerFrame, text="No", activeforeground= "blue", command=confirm_window.destroy)
            no.pack()
        except Exception as error:
            print(f"Error deleting checklist. Error was: {error}")
    def delete_checklist(self, confirm_window):
        if os.path.exists(self.json_path):
            os.remove(self.json_path)
        confirm_window.destroy()
        self.window.destroy()
    def due_date_alert(self):
        try:
            due_soon = []
            due_today = []
            past_due = []
            current_date = datetime.now().date()
            for task in self.task_status:
                if len(self.task_status[task]) > 1:
                    date = self.task_status[task][1]
                    due_date = datetime.strptime(date, "%m/%d/%Y").date()
                    if self.task_status[task][0] == 0:
                        if due_date < current_date:
                            past_due.append(task)
                        elif due_date == current_date:
                            due_today.append(task)
                        elif (due_date - current_date).days <= 2: # if task is due in two days or less
                            due_soon.append(task)
            if len(due_soon) > 0 or len(past_due) > 0 or len(due_today) > 0: # if at least one alert exists
                alert_window = tk.Toplevel(self.window)
                alert_window.title("Alert!")
                alert_window.lift()  # Raises the alert window above the main window
                ok_frame = tk.Frame(alert_window)
                ok_frame.pack(side=tk.BOTTOM)
                ok = tk.Button(ok_frame, text="Ok", command=alert_window.destroy)
                ok.pack(side="bottom")
            bullet_point = "\u2022"
            if len(due_soon) > 0:
                alert_display = ""
                for i in due_soon:
                    if i == due_soon[-1]:
                        alert_display += f"{bullet_point} {i}"
                    else:
                        alert_display += f"{bullet_point} {i}\n"
                soon_frame = tk.Frame(alert_window)
                soon_frame.pack(side=tk.TOP)
                if len(due_soon) == 1:
                    alert_text = 'The following task is due soon:'
                else:
                    alert_text = 'The following tasks are due soon:'
                alert_label = tk.Label(soon_frame, text = alert_text)
                alert_label.pack()
                task_label = tk.Label(soon_frame, text = alert_display)
                task_label.pack()
            if len(past_due) > 0:
                alert_display = ""
                for i in past_due:
                    if i == past_due[-1]:
                        alert_display += f"{bullet_point} {i}"
                    else:
                        alert_display += f"{bullet_point} {i}\n"
                past_frame = tk.Frame(alert_window)
                past_frame.pack(side=tk.TOP)
                if len(past_due) == 1:
                    alert_text = 'The following task is past due:'
                else:
                    alert_text = 'The following tasks are past due:'
                alert_label = tk.Label(past_frame, text = alert_text)
                alert_label.pack()
                task_label = tk.Label(past_frame, text = alert_display)
                task_label.pack()
            if len(due_today) > 0:
                alert_display = ""
                for i in due_today:
                    if i == due_today[-1]:
                        alert_display += f"{bullet_point} {i}"
                    else:
                        alert_display += f"{bullet_point} {i}\n"
                today_frame = tk.Frame(alert_window)
                today_frame.pack(side=tk.TOP)
                if len(due_today) == 1:
                    alert_text = 'The following task is due today:'
                else:
                    alert_text = 'The following tasks are due today:'
                alert_label = tk.Label(today_frame, text = alert_text)
                alert_label.pack()
                task_label = tk.Label(today_frame, text = alert_display)
                task_label.pack()
        except Exception:
            print("Could not display alert window")
    def export_to_file(self, entry, file_window):
        file_input = entry.get()
        if file_input:
            file_name = f"{file_input}.md"
            msg_frame = tk.Frame(file_window)
            msg_frame.pack()
            if len(self.task_status) == 0:
                msg_label = tk.Label(msg_frame, text = "This checklist can not be exported because it is empty")
                msg_label.pack()
            else:
                export_path = os.path.join(os.getcwd(), f"docs/{file_name}")
                with open(export_path, "w") as out_file:
                    for task in self.task_status:
                        if len(self.task_status[task]) > 1:
                            status = self.task_status[task][0]
                            due_date = self.task_status[task][1]
                            if status == 0:
                                out_file.write(f"- [ ] {task} (Due Date: {due_date})\n")
                            else:
                                out_file.write(f"- [x] {task} (Due Date: {due_date})\n")
                        else:
                            status = self.task_status[task][0]
                            if status == 0:
                                out_file.write(f"- [ ] {task}\n")
                            else:
                                out_file.write(f"- [x] {task}\n")     
                msg_label = tk.Label(msg_frame, text = f"{file_name} has been created in the docs directory.")
                msg_label.pack()

    def get_file_name(self):
        try:
            file_window = tk.Toplevel(self.window)
            file_frame = tk.Frame(file_window)
            file_frame.pack()
            exit_file_frame = tk.Frame(file_window)
            exit_file_frame.pack()
            file_label = tk.Label(file_frame, text = "Please enter a file name for your file: ")
            file_label.pack()
            entry = tk.Entry(file_frame)
            entry.pack(fill=tk.X, side=tk.LEFT)
            enter_button = tk.Button(file_frame, text="Enter", activeforeground= "blue", command=lambda: self.export_to_file(entry, file_window))
            enter_button.pack()
            exit_button = tk.Button(exit_file_frame, text="Exit", activeforeground= "blue", command=file_window.destroy)
            exit_button.pack(side=tk.LEFT, padx=10)
        except Exception as error:
            print(f"Error exporting list to a markdown file. Error was: {error}")
    def get_existing_list(self):
        try:
            with open(self.json_path, 'r') as in_file:
                self.task_status = json.load(in_file)
            self.add_existing_tasks()
            # self.due_date_alert()
        except json.decoder.JSONDecodeError:# data is showing up as empty
            print("Data does not exist or can not be read. Creating new to do list.")
            self.task_status = {}