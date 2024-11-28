import os
import json
from PIL import Image

def load_instructions(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:  # Указан encoding для поддержки кириллицы
            instructions = json.load(file)
        return instructions
    except FileNotFoundError:
        print("Файл с инструкциями не найден.")
        return {}
    except json.JSONDecodeError:
        print("Ошибка чтения файла с инструкциями.")
        return {}
    except Exception as e:  # Обработка других возможных исключений
        print(f"Произошла ошибка: {e}")
        return {}


def show_instruction(instruction):
    img_shown = False

    if 'text' in instruction:
        print(f"Инструкция: {instruction['text']}")
    else:
        print("Инструкция отсутствует.")
        return

    if 'image' in instruction and not img_shown:
        try:
            img = Image.open(instruction['image'])
            img.show()
            img_shown = True  # Устанавливаем флаг после показа картинки
        except FileNotFoundError:
            print("Изображение не найдено.")
        except Exception as e:
            print(f"Ошибка при открытии изображения: {e}")

def log_issue(issue, file_path):
    with open(file_path, "a") as file:
        file.write(issue + "\n")

def make_note(note, file_path):
    with open(file_path, "a") as file:
        file.write(note + "\n")

def show_notes(file_path):
    try:
        with open(file_path, "r") as file:
            notes = file.readlines()
            if notes:
                print("\nСписок заметок:")
                for note in notes:
                    print(f"- {note.strip()}")
            else:
                print("Заметок нет.")
    except FileNotFoundError:
        print("Файл с заметками не найден.")

def main():
    instructions = load_instructions("instructions.json")
    issues_file = "issues.txt"
    notes_file = "notes.txt"

    while True:
        print("\n1. Показать инструкции")
        print("2. Сообщить о проблеме")
        print("3. Сделать заметку")
        print("4. Показать заметки")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            for key, instruction in instructions.items():
                print(f"\n{key}:")
                show_instruction(instructions)

        elif choice == '2':
            issue = input("Введите описание проблемы: ")
            log_issue(issue, issues_file)
            print("Проблема зарегистрирована.")

        elif choice == '3':
            note = input("Введите заметку: ")
            make_note(note, notes_file)
            print("Заметка сохранена.")

        elif choice == '4':
            show_notes(notes_file)

        elif choice == '5':
            print("Выход.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
