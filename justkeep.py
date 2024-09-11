import tkinter as tk
from tkinter import messagebox

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        master.title("To Do List")

        self.entry_frame = tk.Frame(master) #фрейм для ввода задачи
        self.entry_frame.pack()

        self.task_label = tk.Label(self.entry_frame, text="Новая задача:")
        self.task_label.pack(side=tk.LEFT)

        self.task_entry = tk.Entry(self.entry_frame)
        self.task_entry.pack(side=tk.LEFT)

        self.add_button = tk.Button(self.entry_frame, text="Добавить", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        self.task_list_frame = tk.Frame(master) #фейм для списка задач
        self.task_list_frame.pack()

        self.task_list = tk.Listbox(self.task_list_frame, width=50)
        self.task_list.pack()

        self.delete_button = tk.Button(self.task_list_frame, text="Удалить", command=self.delete_task)
        self.delete_button.pack()

        self.load_tasks()  #загрузка задач из файла

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.task_list.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Предупреждение", "Введите задачу!")

    def delete_task(self):
        try:
            selection = self.task_list.curselection()[0]
            self.task_list.delete(selection)
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления!")

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.task_list.get(0, tk.END):
                file.write(task + "\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                for task in file:
                    self.task_list.insert(tk.END, task.strip())
        except FileNotFoundError:
            pass

root = tk.Tk() #создание главного окна и запуска приложения
app = ToDoListApp(root)
root.mainloop()