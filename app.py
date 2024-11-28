import tkinter as tk
from tkinter import Tk, Label, messagebox, Toplevel
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

        # Текст инструкции с увеличенным размером шрифта
        instruction_label = Label(
            instruction_window,
            text=instruction['text'],
            wraplength=720,
            font=("Arial", 18)
        )
        instruction_label.pack(pady=10)

        # Изображение инструкции
        if 'image' in instruction:
            try:
                img = Image.open(instruction['image'])
                img = img.resize((1280, 720), Image.LANCZOS)  # Изменяем размер изображения
                photo = ImageTk.PhotoImage(img)

                img_label = Label(instruction_window, image=photo)
                img_label.image = photo  # Сохраняем ссылку на изображение
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
        show_notes()
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
    global instruction_text, note_entry, notes_list

    root = tk.Tk()
    root.title("Инструкции и Заметки")

    instruction_text = tk.StringVar()
    note_entry = tk.Entry(root, width=100, font=('Arial', 20))
    notes_list = tk.Listbox(root, width=100, height=8, font=('Arial', 18))

    # Конструируем интерфейс с увеличенными размерами
    tk.Button(root, text="Открыть инструкции", command=open_instructions, width=25, height=2, font=('Arial', 18)).pack(pady=10)
    tk.Label(root, textvariable=instruction_text, wraplength=400, font=('Arial', 20)).pack(pady=10)
    tk.Label(root, text="Добавить заметку или сообщение об ошибке:", font=('Arial', 20)).pack(pady=5)
    note_entry.pack(pady=10)
    tk.Button(root, text="Сохранить заметку", command=make_note, width=25, height=2, font=('Arial', 18)).pack(pady=10)
    tk.Button(root, text="Показать заметки", command=show_notes, width=25, height=2, font=('Arial', 18)).pack(pady=10)

    tk.Button(root, text="Сообщить об ошибке", command=log_issue, width=25, height=2, font=('Arial', 18)).pack(pady=10)
    tk.Button(root, text="Показать записи об ошибках", command=show_issues, width=25, height=2, font=('Arial', 18)).pack(pady=10)
    notes_list.pack(pady=10)

    # Настроим отступы и размеры для улучшения пользовательского интерфейса
    for widget in [note_entry, notes_list]:
        widget.config(font=('Arial', 20))

    # Начинаем главный цикл
    root.mainloop()