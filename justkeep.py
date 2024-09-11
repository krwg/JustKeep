import tkinter as tk
from tkinter import messagebox

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        master.title("JustKeep")

        header_frame = tk.Frame(master, bg="#f0f0f0")
        header_frame.pack(fill="x")
        header_label = tk.Label(header_frame, text="To Do", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        header_label.pack(pady=10)

        self.entry_frame = tk.Frame(master, bg="#f0f0f0")
        self.entry_frame.pack(fill="x", pady=10)

        self.task_label = tk.Label(self.entry_frame, text="Новая задача:", bg="#f0f0f0", fg="#333", font=("Arial", 12))
        self.task_label.pack(side=tk.LEFT, padx=10)

        self.task_entry = tk.Entry(self.entry_frame, bg="#fff", fg="#333", font=("Arial", 12))
        self.task_entry.pack(side=tk.LEFT, padx=10)

        self.add_button = tk.Button(self.entry_frame, text="Добавить", command=self.add_task, bg="#4CAF50", fg="#fff", font=("Arial", 10, "bold"))
        self.add_button.pack(side=tk.LEFT, padx=10)

        # Фрейм для списка задач
        self.task_list_frame = tk.LabelFrame(master, text="Список задач", bg="#f0f0f0", font=("Arial", 12, "bold"), fg="#333")
        self.task_list_frame.pack(pady=10)

        self.task_list = tk.Listbox(self.task_list_frame, width=50, bg="#fff", fg="#333", font=("Arial", 12))
        self.task_list.pack()

        self.delete_button = tk.Button(self.task_list_frame, text="Удалить", command=self.delete_task, bg="#f44336", fg="#fff", font=("Arial", 10, "bold"))
        self.delete_button.pack()

        self.load_tasks()

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

root = tk.Tk()
app = ToDoListApp(root)
root.mainloop()