import argparse
import csv
import os
import runpy
import zipfile
from tkinter import Tk, Text, Entry, END, StringVar

VIRTUAL_FS_ROOT = '/'  # Корневая директория виртуальной ФС будет внутри архива
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))  # Корневая директория

# Переменная для хранения открытого zip-архива
zip_fs = None


# Парсинг аргументов командной строки
def parse_args():
    parser = argparse.ArgumentParser(description="Эмулятор оболочки")
    parser.add_argument('--user', required=True, help="Имя пользователя")
    parser.add_argument('--filesystem', required=True, help="Путь к zip-файлу виртуальной ФС")
    parser.add_argument('--logfile', required=True, help="Путь к лог-файлу")
    parser.add_argument('--script', required=False, help="Путь к стартовому скрипту")
    return parser.parse_args()


# Логирование действий
def log_action(user, action, log_file):
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user, action])


# Проверка, что путь находится внутри виртуальной файловой системы
def is_within_virtual_fs(path):
    return path.startswith(VIRTUAL_FS_ROOT)


# Открытие виртуальной файловой системы
def open_filesystem(zip_path):
    global zip_fs
    if zipfile.is_zipfile(zip_path):
        zip_fs = zipfile.ZipFile(zip_path, 'r')
        zip_fs.close()
    else:
        raise FileNotFoundError("Недопустимый zip-файл")


# Проверка существования файла или директории
def path_exists(path):
    normalized_path = path.lstrip('/')  # Убираем ведущий слэш
    if normalized_path == '/':  # Корневая директория всегда существует
        return True
    for file_info in zip_fs.infolist():
        if file_info.filename.startswith(normalized_path):
            return True
    return False


# Чтение файлов внутри zip-архива
def list_files_in_directory(directory):
    normalized_directory = directory.lstrip('/')  # Убираем ведущий слэш
    files = set()
    for file_info in zip_fs.infolist():
        # Проверяем, что файл находится в указанной директории
        if file_info.filename.startswith(normalized_directory):
            relative_path = file_info.filename[len(normalized_directory):].strip('/')
            if '/' not in relative_path and relative_path != '':
                files.add(relative_path)
            elif '/' in relative_path:
                files.add(relative_path.split('/')[0])
    return list(files)


# Создание файла roots.txt, если его нет
def create_roots_file():
    open(os.path.join(SCRIPT_DIR, 'roots.txt'), 'a').close()


# Выполнение Python-скрипта
def execute_python_script(script_path):
    if os.path.exists(script_path) and script_path.endswith('.py'):
        runpy.run_path(script_path)
    else:
        raise FileNotFoundError(f"Скрипт {script_path} не найден или не является Python-скриптом")


# Чтение информации из roots.txt
def read_roots_file():
    roots_file = os.path.join(SCRIPT_DIR, 'roots.txt')
    roots_data = {}
    if os.path.exists(roots_file):
        with open(roots_file, 'r') as file:
            for line in file:
                path, mode = line.strip().split(' ')
                roots_data[path] = mode
    return roots_data


# Запись информации в roots.txt, с перезаписью существующей записи
def write_roots_file(path, mode):
    roots_file = os.path.join(SCRIPT_DIR, 'roots.txt')
    roots_data = read_roots_file()
    roots_data[path] = mode

    # Перезаписываем файл
    with open(roots_file, 'w') as file:
        for file_path, file_mode in roots_data.items():
            file.write(f'{file_path} {file_mode}\n')


# Выполнение команд
def execute_command(command, user, log_file, output=None, current_directory=VIRTUAL_FS_ROOT):
    command = command.strip()

    def print_output(message):
        if output is None:
            return
        if hasattr(output, 'insert'):
            output.insert(END, message + '\n')
        else:
            output.write(message + '\n')

    # Обработчик команды exit
    def quit_shell():
        if 'root' in globals():  # Для GUI
            root.quit()
        else:
            raise SystemExit()

    # Команда "exit"
    if command == 'exit':
        quit_shell()
        log_action(user, 'exit', log_file)

    elif command == 'whoami':
        print_output(user)
        log_action(user, 'whoami', log_file)

    elif command == 'pwd':
        normalized_path = os.path.normpath(current_directory)
        print_output(normalized_path)
        log_action(user, 'pwd', log_file)

    elif command.startswith('ls'):
        parts = command.split()
        long_format = '-l' in parts  # Проверка на наличие флага -l
        roots_data = read_roots_file()  # Чтение данных из roots.txt

        # Определение пути
        if len(parts) > 1 and parts[-1] != '-l':
            path = os.path.normpath(os.path.join(current_directory, parts[-1])).replace('\\', '/')
        else:
            path = current_directory.replace('\\', '/')  # Если путь не указан, используем текущую директорию
        if is_within_virtual_fs(path):  # Проверяем, что путь внутри виртуальной ФС
            if path_exists(path):  # Проверка на существование пути
                files = list_files_in_directory(path)
                if long_format:
                    if len(files) == 0 and '.' in path:
                        print_output(f'{roots_data.get(path)} {parts[-1]}')
                    for file in files:
                        file_path = os.path.normpath(os.path.join(path, file)).replace('\\', '/')
                        file_permissions = roots_data.get(file_path)
                        if file_permissions:
                            print_output(f'{file_permissions} {file}')
                        else:
                            print_output(f'Права для {file} не найдены в roots.txt')
                else:
                    print_output(' '.join(files))
            else:
                print_output('Не удалось найти файл/директорию по указанному пути!')
            if long_format:
                log_action(user, 'ls -l ' + os.path.normpath(path), log_file)
            else:
                log_action(user, 'ls ' + os.path.normpath(path), log_file)
        else:
            print_output('Ошибка: выход за пределы виртуальной ФС')

    elif command.startswith('cd'):
        parts = command.split()
        if len(parts) == 1 or parts[1] == "~":
            # Если нет аргументов или указан символ ~, возвращаемся в корень
            current_directory = VIRTUAL_FS_ROOT
        else:
            # Формируем новый путь
            new_dir = os.path.normpath(os.path.join(current_directory, parts[1])).replace('\\', '/')
            # Проверяем, находится ли новый путь внутри виртуальной файловой системы
            if path_exists(new_dir) and is_within_virtual_fs(new_dir):
                current_directory = new_dir  # Обновляем текущую директорию
            else:
                print_output('Ошибка: выход за пределы виртуальной ФС или такой директории нет')
                return current_directory  # Возвращаем текущую директорию

        log_action(user, 'cd ' + current_directory, log_file)

    elif command.startswith('chmod'):
        parts = command.split()
        if len(parts) == 3:
            mode, path = parts[1], os.path.normpath(os.path.join(current_directory, parts[2])).replace('\\', '/')
            if is_within_virtual_fs(path):  # Проверка, что путь внутри виртуальной ФС
                # Вносим изменения в файл roots.txt
                write_roots_file(path, mode)

                print_output(f'Режим доступа для {path} изменён на {mode}')
                log_action(user, f'chmod {mode} {path}', log_file)
            else:
                print_output('Ошибка: выход за пределы виртуальной ФС')
        else:
            print_output('Неправильная команда chmod')

    else:
        print_output('Неизвестная команда')

    return current_directory


# Выполнение команд из текстового файла
def execute_script_commands(script_path, user, log_file, output, current_directory=VIRTUAL_FS_ROOT):
    if os.path.exists(script_path) and script_path.endswith('.txt'):
        with open(script_path, 'r') as file:
            for line in file:
                # Выводим команду на экран
                output.insert(END, f'{user}@shell:~$ {line.strip()}\n')
                # Выполняем команду
                current_directory = execute_command(line.strip(), user, log_file, output,
                                                    current_directory=current_directory)
    else:
        raise FileNotFoundError(f"Скрипт {script_path} не найден или не является текстовым файлом")
    return current_directory


# GUI функции
def on_enter(event, input_var, output, user, log_file, current_directory_var):
    command = input_var.get()
    output.insert(END, f'{user}@shell:~$ {command}\n')
    input_var.set("")

    # Выполняем команду и обновляем директорию
    new_directory = execute_command(command, user, log_file, output, current_directory_var.get())
    current_directory_var.set(new_directory)


# Запуск GUI
def start_gui(user, log_file, script=None):
    # Создаём окно и текстовое поле для вывода
    global root
    root = Tk()
    root.title("Эмулятор shell")
    output = Text(root, height=25, width=100)
    output.pack()

    input_var = StringVar()
    input_entry = Entry(root, textvariable=input_var, width=30)
    input_entry.pack()

    # Используем StringVar для отслеживания текущей директории
    current_directory_var = StringVar(value=VIRTUAL_FS_ROOT)

    # Привязываем обработчик для ввода команд
    input_entry.bind("<Return>",
                     lambda event: on_enter(event, input_var, output, user, log_file, current_directory_var))

    # Выполняем стартовый скрипт (если указан)
    if script:
        if script.endswith('.txt'):
            try:
                # Выводим заголовок перед выполнением скрипта
                output.insert(END, f"Выполнение команд из {script}:\n")
                current_directory = execute_script_commands(script, user, log_file, output, current_directory_var.get())
                current_directory_var.set(current_directory)
            except FileNotFoundError as e:
                output.insert(END, f"Ошибка: {e}\n")
        else:
            try:
                execute_python_script(script)
            except FileNotFoundError as e:
                output.insert(END, f"Ошибка: {e}\n")

    # Запускаем основной цикл обработки событий Tkinter
    root.mainloop()


if __name__ == "__main__":
    args = parse_args()
    # Открываем виртуальную файловую систему
    open_filesystem(args.filesystem)
    # Логируем запуск
    log_action(args.user, 'Session start', args.logfile)
    # Создаём файл roots.txt, если его нет
    create_roots_file()
    # Запуск GUI
    start_gui(args.user, args.logfile, script=args.script)
