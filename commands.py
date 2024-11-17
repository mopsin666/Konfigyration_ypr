import os
import zipfile
import io

# Команда 'ls' — выводит список файлов и директорий в текущей директории.
def ls(path):
    return "\n".join(os.listdir(path))

# Команда 'cd' — меняет текущую рабочую директорию.
def cd(path, current_directory):
    # Проверим, существует ли путь.
    if os.path.isdir(path):
        return os.path.join(current_directory, path)
    else:
        raise FileNotFoundError(f"cd: {path}: No such file or directory")

# Команда 'chmod' — изменяет права доступа к файлу.
def chmod(path, mode):
    os.chmod(path, mode)
    return f"chmod: {path} permissions changed to {oct(mode)}"

# Команда 'echo' — выводит строку на экран.
def echo(text):
    return text

# Команда 'uniq' — удаляет повторяющиеся строки в текстовом файле.
def uniq(path):
    with open(path, 'r') as file:
        lines = file.readlines()
    return ''.join(sorted(set(lines), key=lines.index))  # Удаляет дубликаты строк, сохраняя порядок.
