import tkinter as tk
from tkinter import messagebox, ttk, StringVar, Entry
from tkinter import filedialog
from PIL import Image, ImageTk 
import os

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        master.title("JustKeep")

        #иконка приложения
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            master.iconbitmap(icon_path)

        #стиль для виджетов
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabelframe.Label", font=("Arial", 12, "bold"))

        #фрейм для заголовка
        header_frame = tk.Frame(master, bg="#f0f0f0")
        header_frame.pack(fill="x")
        header_label = tk.Label(header_frame, text="JustKeep", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
        header_label.pack(pady=10)

        #фрейм для основного содержимого
        content_frame = tk.Frame(master)
        content_frame.pack(pady=10)

        #фрейм для ввода задач
        self.entry_frame = tk.Frame(content_frame, bg="#f0f0f0")
        self.entry_frame.pack(fill="x", pady=5)

        #поле ввода задачи
        self.task_entry = tk.Entry(self.entry_frame, bg="#fff", fg="#333", font=("Arial", 12))
        self.task_entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        #кнопка добавления задачи
        self.add_button = ttk.Button(self.entry_frame, text="Добавить", command=self.add_task, width=10)
        self.add_button.pack(side=tk.LEFT, padx=10)

        #фрейм для поиска и сортировки
        self.search_sort_frame = tk.Frame(content_frame)
        self.search_sort_frame.pack(fill="x", pady=5)

        #поле поиска
        self.search_entry = Entry(self.search_sort_frame, bg="#fff", fg="#333", font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        self.search_entry.bind("<KeyRelease>", self.search_tasks)

        #кнопка сортировки
        self.sort_button = ttk.Button(self.search_sort_frame, text="Сортировать", command=self.sort_tasks, width=10)
        self.sort_button.pack(side=tk.LEFT, padx=10)

        #фрейм для списка задач
        self.task_list_frame = ttk.Labelframe(content_frame, text="Список задач")
        self.task_list_frame.pack(pady=5, expand=True, fill=tk.BOTH)

        #список задач
        self.task_list = tk.Listbox(self.task_list_frame, width=50, bg="#fff", fg="#333", font=("Arial", 12), selectbackground="#4CAF50", selectforeground="#fff")
        self.task_list.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        #фрейм для кнопок рядом с задачами
        self.button_frame = tk.Frame(self.task_list_frame)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y)

        #кнопка удаления задачи
        self.delete_button = ttk.Button(self.button_frame, text="Удалить", command=self.delete_task, width=10)
        self.delete_button.pack(pady=5)

        #кнопка для галочки
        self.toggle_button = ttk.Button(self.button_frame, text="Галочка", command=self.toggle_task_completion, width=10)
        self.toggle_button.pack(pady=5)

        #кнопка редактирования задачи
        self.edit_button = ttk.Button(self.button_frame, text="Редактировать", command=self.edit_task, width=10)
        self.edit_button.pack(pady=5)

        #загрузка задач из файла
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

    def toggle_task_completion(self):
        try:
            selection = self.task_list.curselection()[0]
            task = self.task_list.get(selection)

            if task.startswith("✔ "):
                self.task_list.delete(selection)
                self.task_list.insert(selection, task[3:])
            else:
                self.task_list.delete(selection)
                self.task_list.insert(selection, "✔ " + task)

            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите задачу для изменения статуса!")

    def edit_task(self):
        try:
            selection = self.task_list.curselection()[0]
            task = self.task_list.get(selection)

            #диалоговое окно для редактирования
            edit_window = tk.Toplevel(self.master)
            edit_window.title("Изменить")

            edit_label = tk.Label(edit_window, text="Измените задачу:")
            edit_label.pack(pady=5)

            edit_entry = Entry(edit_window, bg="#fff", fg="#333", font=("Arial", 12))
            edit_entry.insert(0, task)
            edit_entry.pack(pady=5)

            def save_edit():
                new_task = edit_entry.get()
                self.task_list.delete(selection)
                self.task_list.insert(selection, new_task)
                self.save_tasks()
                edit_window.destroy()

            save_button = ttk.Button(edit_window, text="Сохранить", command=save_edit, width=10)
            save_button.pack(pady=5)

        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования!")

    def search_tasks(self, event=None):
        search_term = self.search_entry.get().lower()
        self.task_list.delete(0, tk.END)
        for i in range(len(self.tasks)):
            if search_term in self.tasks[i].lower():
                self.task_list.insert(tk.END, self.tasks[i])

    def sort_tasks(self):
        #реализация сортировки
        pass

    def save_tasks(self):
        self.tasks = [self.task_list.get(i) for i in range(self.task_list.size())]
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = [task.strip() for task in file]
                for task in self.tasks:
                    self.task_list.insert(tk.END, task)
        except FileNotFoundError:
            pass

root = tk.Tk()
app = ToDoListApp(root)
root.mainloop()