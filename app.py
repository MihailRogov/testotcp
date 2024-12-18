import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import json
from PIL import Image, ImageTk


def load_instructions(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл с инструкциями не найден.")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", "Ошибка чтения файла с инструкциями.")
        return {}
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
        return {}


def show_instruction(instruction):
    if 'text' in instruction:
        instruction_window = Toplevel()
        instruction_window.title("Инструкция")
        instruction_window.geometry("800x600")
        instruction_window.configure(bg="#f4f4f4")

        # Текст инструкции с увеличенным размером шрифта
        instruction_label = tk.Label(
            instruction_window,
            text=instruction['text'],
            wraplength=720,
            font=("Arial", 16),
            bg="#f4f4f4",
            fg="#333333"
        )
        instruction_label.pack(pady=10)

        # Изображение инструкции
        if 'image' in instruction:
            try:
                img = Image.open(instruction['image'])
                img = img.resize((640, 360), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                img_label = tk.Label(instruction_window, image=photo, bg="#f4f4f4")
                img_label.image = photo
                img_label.pack(pady=10)
            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Изображение не найдено.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при открытии изображения: {e}")
    else:
        messagebox.showinfo("Инструкция", "Инструкция отсутствует.")


def log_issue():
    note = note_entry.get()
    if note:
        with open("issues.txt", "a") as file:
            file.write('-' + note + "\n")
        note_entry.delete(0, 'end')
        show_issues()
    else:
        messagebox.showwarning("Предупреждение", "Введите сообщение об ошибке.")


def show_issues():
    try:
        with open("issues.txt", "r") as file:
            notes = file.readlines()
            notes_list.delete(0, tk.END)
            for note in notes:
                notes_list.insert(tk.END, note.strip())
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл с ошибками не найден.")


def make_note():
    note = note_entry.get()
    if note:
        with open("notes.txt", "a") as file:
            file.write('-' + note + "\n")
        note_entry.delete(0, 'end')
        show_notes()
    else:
        messagebox.showwarning("Предупреждение", "Введите заметку.")


def show_notes():
    try:
        with open("notes.txt", "r") as file:
            notes = file.readlines()
            notes_list.delete(0, tk.END)
            for note in notes:
                notes_list.insert(tk.END, note.strip())
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл с заметками не найден.")


def open_instructions():
    file_path = "instructions.json"
    instructions = load_instructions(file_path)
    if instructions:
        show_instruction(instructions)


def main():
    global note_entry, notes_list

    root = tk.Tk()
    root.title("Инструкции и Заметки")
    root.geometry("900x700")
    root.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 14), padding=10)
    style.configure("TLabel", font=("Arial", 14), background="#f0f0f0")

    tk.Label(root, text="Управление инструкциями и заметками", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

    ttk.Button(root, text="Открыть инструкции", command=open_instructions).pack(pady=10)

    tk.Label(root, text="Добавить заметку или сообщение об ошибке:", font=("Arial", 16), bg="#f0f0f0").pack(pady=5)

    note_entry = ttk.Entry(root, width=60, font=("Arial", 14))
    note_entry.pack(pady=10)

    ttk.Button(root, text="Сохранить заметку", command=make_note).pack(pady=5)
    ttk.Button(root, text="Показать заметки", command=show_notes).pack(pady=5)

    ttk.Button(root, text="Сообщить об ошибке", command=log_issue).pack(pady=5)
    ttk.Button(root, text="Показать записи об ошибках", command=show_issues).pack(pady=5)

    notes_list = tk.Listbox(root, width=70, height=10, font=("Arial", 14))
    notes_list.pack(pady=20)

    root.mainloop()

