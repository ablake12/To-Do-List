import curses
class ToDoList:
    def __init__(self):
        self.tasks = []
        self.current_task_index = 1
    def addTasks(self, task):
        task_num = len(self.tasks) + 1
        self.tasks.append({task_num: task, "completed": False})
    def displayTasks(self):
        if len(self.tasks) > 0:
            for task in self.tasks:
                if task['completed']: 
                    print(f"[X] {task[next(iter(task))]}")
                else:
                    print(f"[ ] {task[next(iter(task))]}")
        else:
            print("Your list is empty")
    def deleteTask(self):
        for task in self.tasks:
            for key in task.keys():
                if key != "completed":
                    print(f"{key}. {task[key]}")
        # deleteInput = input("Please choose a task to delete (Ex: 1, 3): ")
        # while not deleteInput.isnumeric() and deleteInput < 0 and deleteInput > len(self.tasks) + 1:
        #     deleteInput = input(f"{deleteInput} is an invalid response.\nPlease choose a task to delete (Ex: 1, 3): ")
        if len(self.tasks) > 0:
            while True:
                deleteInput = input("Please choose a task to delete (Ex: 1): ")

                if not deleteInput.isdigit() or int(deleteInput) < 1 or int(deleteInput) > len(self.tasks):
                    print(f"{deleteInput} is an invalid response.")
                else:
                    deleteInput = int(deleteInput)
                    break
            self.tasks.pop(deleteInput - 1)

            for i in range(len(self.tasks)):
                new_key = i + 1
                for key in list(self.tasks[i].keys()):
                    if key != 'completed':
                        if new_key != key:
                            self.tasks[i][new_key] = self.tasks[i].pop(key)
        else:
            print("Your list is empty")
    def markTasks(self, num):
        if 0 < num <= len(self.tasks):
            index = num - 1
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        else:
            print("Invalid task index")

    def process_user_input(self, stdscr):
        key = stdscr.getch()
        if key == curses.KEY_UP:
            self.current_task_index = max(0, self.current_task_index - 1)
        elif key == curses.KEY_DOWN:
            self.current_task_index = min(len(self.tasks) - 1, self.current_task_index + 1)
        elif key == ord(" "):
            self.markTasks(self.current_task_index)
        elif key == ord("q"):
            return False
        return True

def main(stdscr):
    to_do = ToDoList()
    to_do.addTasks("Go to target")
    to_do.addTasks("Write thank you cards")
    to_do.addTasks("Bake cookies")
    to_do.displayTasks()
    to_do.deleteTask()
    to_do.process_user_input(stdscr)
    to_do.displayTasks()
    to_do.deleteTask()

# if __name__ == "__main__":
#     curses.wrapper(main)