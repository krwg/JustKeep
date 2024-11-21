import tkinter as tk
import customtkinter
import sqlite3
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

#dev.krwg

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

def db_start():
    global conn, cur
    try:
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        customtkinter.CTkMessageBox(title="Ошибка", message="Ошибка подключения к базе данных.")

def save_note(event=None):
    note = note_entry.get("1.0", tk.END).strip()
    if note:
        try:
            cur.execute("INSERT INTO notes (note) VALUES (?)", (note,))
            conn.commit()
            update_notes_list()
            note_entry.delete("1.0", tk.END)
        except sqlite3.Error as e:
            print(f"Ошибка сохранения заметки: {e}")
            customtkinter.CTkMessageBox(title="Ошибка", message="Ошибка сохранения заметки.")
    else:
        customtkinter.CTkMessageBox(title="Предупреждение", message="Заметка пуста!")

def update_notes_list():
    notes_list.delete(0, tk.END)
    for widget in note_container_frame.winfo_children():
        widget.destroy()
    try:
        cur.execute("SELECT id, note FROM notes")
        notes = cur.fetchall()
        if notes:
            notes_label.configure(text="")
            instruction_label.grid_forget()
            for i, (note_id, note_text) in enumerate(notes):
                notes_list.insert(tk.END, note_text)
                create_note_container(note_text, i, note_id)
        else:
            notes_label.configure(text="Здесь будут ваши заметки")
            instruction_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
    except sqlite3.Error as e:
        print(f"Ошибка обновления списка заметок: {e}")
        customtkinter.CTkMessageBox(title="Ошибка", message="Ошибка обновления списка заметок.")

def create_note_container(note_text, row_index, note_id):
    container = customtkinter.CTkFrame(note_container_frame, fg_color="transparent", corner_radius=5, border_width=2, border_color="#555555")
    container.grid(row=row_index, column=0, sticky="nsew", padx=10, pady=(5, 0))
    container.columnconfigure(0, weight=1)

    label = customtkinter.CTkLabel(container, text=note_text, font=("Arial", 12), text_color="lightgray", anchor="w", justify="left", wraplength=300)
    label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    container.rowconfigure(0, weight=1)

    menu = tk.Menu(container, tearoff=0)
    menu.add_command(label="Удалить", command=lambda id=note_id: delete_note_by_id(id))
    menu.add_command(label="Изменить", command=lambda id=note_id: edit_note(id))

    label.bind("<Button-3>", lambda event, menu=menu: menu.post(event.x_root, event.y_root))
    label.bind("<Button-1>", lambda event, text=note_text: copy_to_editor(text))

    return container

def delete_note_by_id(note_id):
    try:
        cur.execute("DELETE FROM notes WHERE id=?", (note_id,))
        conn.commit()
        update_notes_list()
    except sqlite3.Error as e:
        print(f"Ошибка удаления заметки: {e}")
        customtkinter.CTkMessageBox(title="Ошибка", message="Ошибка удаления заметки.")

def copy_to_editor(note_text):
    note_entry.delete("1.0", tk.END)
    note_entry.insert("1.0", note_text)

def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))

settings_window = None
selected_section = None

def open_settings():
    global settings_window, selected_section
    if settings_window is None or not settings_window.winfo_exists():
        settings_window = customtkinter.CTkToplevel(root)
        settings_window.title("Настройки")
        settings_window.geometry("600x300")
        settings_window.resizable(False, False)

        left_settings_column = customtkinter.CTkFrame(settings_window, fg_color="#333333")
        left_settings_column.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        right_settings_column = customtkinter.CTkFrame(settings_window, fg_color="#222222")
        right_settings_column.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        settings_sections = {
            "Главное": display_main,
            "О приложении": display_about
        }

        for i, (section_name, display_func) in enumerate(settings_sections.items()):
            button = customtkinter.CTkButton(left_settings_column, text=section_name,
                                             command=lambda func=display_func, rc=right_settings_column: select_section(func, rc),
                                             fg_color="#333333",
                                             hover_color=("gray80", "gray40"))
            button.grid(row=i, column=0, sticky="ew", pady=5)

        selected_section = display_about
        selected_section(right_settings_column)

        settings_window.columnconfigure(0, weight=1)
        settings_window.columnconfigure(1, weight=3)
        settings_window.protocol("WM_DELETE_WINDOW", close_settings)

def close_settings():
    global settings_window
    settings_window.destroy()
    settings_window = None

def check_for_updates():
    messagebox.showinfo("Обновления", "У вас последняя версия.")

def select_section(func, right_column):
    global selected_section
    selected_section = func
    clear_right_column(right_column)
    selected_section(right_column)

def clear_right_column(right_column):
    for widget in right_column.winfo_children():
        widget.grid_remove()
        widget.destroy()

def display_about(right_column):
    app_name_label = customtkinter.CTkLabel(right_column, text="JustKeep", font=("Arial", 20), text_color="lightgray")
    app_name_label.pack(pady=5)

    app_desc_label = customtkinter.CTkLabel(right_column, text="Быстрые заметки, без лишних сложностей.", font=("Arial", 14), text_color="lightgray")
    app_desc_label.pack(pady=2)

    author_label = customtkinter.CTkLabel(right_column, text="krwg. 2024", font=("Arial", 10), text_color="lightgray")
    author_label.pack(pady=5)

    version_label = customtkinter.CTkLabel(right_column, text=f"Версия: 1.0 Moonstone", font=("Arial", 12))
    version_label.pack(pady=5)

    check_updates_button = customtkinter.CTkButton(right_column, text="Проверить обновления", command=check_for_updates, fg_color=("gray70", "gray30"), hover_color=("gray80", "gray40"))
    check_updates_button.pack(pady=5)

def display_main(right_column):
    main_label = customtkinter.CTkLabel(right_column, text="В разработке, ожидайте в новой версии", font=("Arial", 12))
    main_label.pack(pady=10)

def edit_note(note_id):
    try:
        cur.execute("SELECT note FROM notes WHERE id=?", (note_id,))
        note_text = cur.fetchone()[0]
        edit_window = customtkinter.CTkToplevel(root)
        edit_window.title("Редактирование заметки")

        edit_textbox = customtkinter.CTkTextbox(edit_window, font=("Arial", 12), fg_color="#444444", text_color="lightgray")
        edit_textbox.insert("0.0", note_text)
        edit_textbox.pack(pady=10, padx=10, fill="both", expand=True)

        def save_edit():
            edited_text = edit_textbox.get("1.0", tk.END).strip()
            cur.execute("UPDATE notes SET note=? WHERE id=?", (edited_text, note_id))
            conn.commit()
            update_notes_list()
            edit_window.destroy()

        save_button = customtkinter.CTkButton(edit_window, text="Сохранить", command=save_edit)
        save_button.pack(pady=10)

    except sqlite3.Error as e:
        print(f"Ошибка редактирования заметки: {e}")
        customtkinter.CTkMessageBox(title="Ошибка", message="Ошибка редактирования заметки.")

def change_theme(is_dark):
    if is_dark:
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")

root = customtkinter.CTk()
root.title("Just Keep")
root.geometry("800x600")
root.resizable(True, True)
try:
    root.iconbitmap("icon.ico")
except tk.TclError:
    print("Иконка не найдена или некорректный формат.")

header = customtkinter.CTkFrame(root, fg_color="transparent")
header.grid(row=0, column=0, columnspan=2, sticky="ew")

header_label = customtkinter.CTkLabel(header, text="JustKeep", font=("Arial", 24))
header_label.pack(pady=10, side=tk.LEFT, expand=True, fill="x")


try:
    image = Image.open("settings_icon.png")
    photo = ImageTk.PhotoImage(image)
    settings_button = customtkinter.CTkButton(header, text="Настройки", image=photo, compound=tk.RIGHT, fg_color=("gray70", "gray30"), hover_color=("gray80", "gray40"), border_width=0)
    settings_button.image = photo
    settings_button.pack(side=tk.RIGHT, padx=10, pady=10)
    settings_button.configure(command=open_settings)
except FileNotFoundError:
    print("Файл с иконкой не найден!")
    settings_button = customtkinter.CTkButton(header, text="Настройки", command=open_settings, fg_color=("gray70", "gray30"), hover_color=("gray80", "gray40"), border_width=0)
    settings_button.pack(side=tk.RIGHT, padx=10, pady=10)



left_canvas = tk.Canvas(root, bg="#333333", highlightthickness=0)
left_canvas.grid(row=1, column=0, sticky="nsew")

notes_label = customtkinter.CTkLabel(left_canvas, text="Здесь будут ваши заметки", font=("Arial", 14), text_color="lightgray")
notes_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

instruction_label = customtkinter.CTkLabel(left_canvas, text="Для создания введите текст и Enter", font=("Arial", 10), text_color="#888888")
instruction_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

note_container_frame = customtkinter.CTkFrame(left_canvas, fg_color="#333333")
note_container_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
note_container_frame.columnconfigure(0, weight=1)

for i in range(100):
    note_container_frame.rowconfigure(i, weight=1)

notes_list = tk.Listbox(left_canvas, width=0, height=0, font=("Arial", 12), bg="#333333", fg="lightgray", selectbackground="#666666", selectforeground="white", exportselection=False)


right_canvas = tk.Canvas(root, bg="#222222", highlightthickness=0)
right_canvas.grid(row=1, column=1, sticky="nsew")

note_label = customtkinter.CTkLabel(right_canvas, text="Заметка:", font=("Arial", 12), text_color="lightgray")
note_entry = customtkinter.CTkTextbox(right_canvas, font=("Arial", 12), fg_color="#444444", text_color="lightgray")
note_entry.bind("<Return>", save_note)
note_entry.bind("<Control-Return>", lambda event: note_entry.insert(tk.END, "\n"))

note_label.pack(pady=10, padx=10)
note_entry.pack(pady=10, padx=10, fill="both", expand=True)


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.rowconfigure(1, weight=1)


root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", toggle_fullscreen)

db_start()
update_notes_list()

root.mainloop()
if conn:
    conn.close()