import os
import zipfile
import argparse
import configparser
import xml.etree.ElementTree as ET
from datetime import datetime

MAX_DEPTH = 5  # Максимальное количество уровней вверх, к которым можно перейти


def log_action(log_file, action):
    tree = ET.parse(log_file)
    root = tree.getroot()

    new_action = ET.Element("action")
    new_action.set("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    new_action.text = action

    root.append(new_action)
    tree.write(log_file)


def setup_logging(log_file):
    root = ET.Element("log")
    tree = ET.ElementTree(root)
    tree.write(log_file)


def extract_vfs(vfs_path, extract_path):
    with zipfile.ZipFile(vfs_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)


def change_directory(base_path, current_path, new_path):
    levels_up = current_path.split(os.sep).count('..')
    if new_path == '..' and levels_up >= MAX_DEPTH:
        print("Error: Maximum directory depth exceeded.")
        return current_path

    new_dir = os.path.normpath(os.path.join(current_path, new_path))
    if not new_dir.startswith(base_path):
        print("Error: Access outside the VFS archive is not allowed.")
        return current_path

    if os.path.isdir(new_dir):
        return new_dir
    else:
        print(f"Error: No such directory: {new_path}")
        return current_path


def list_directory(current_path):
    return os.listdir(current_path)


def list_directory_detailed(current_path):
    items = os.listdir(current_path)
    for item in items:
        item_path = os.path.join(current_path, item)
        mode = os.stat(item_path).st_mode
        permissions = stat.filemode(mode)
        print(f"{permissions} {item}")


def echo_message(message):
    print(message)
    return message


def unique_lines(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: No such file: {os.path.basename(file_path)}")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    unique_lines = list(dict.fromkeys(lines))
    for line in unique_lines:
        print(line, end='')
    return unique_lines


def change_mode(file_path, mode):
    if not os.path.isfile(file_path):
        print(f"Error: No such file: {os.path.basename(file_path)}")
        return
    os.chmod(file_path, int(mode, 8))


def run_start_script(script_path, base_path, current_path):
    with open(script_path, 'r') as file:
        commands = file.readlines()

    for command in commands:
        current_path = execute_command(command.strip(), base_path, current_path)
    return current_path


def execute_command(command, base_path, current_path):
    parts = command.split()
    if len(parts) == 0:
        return current_path

    cmd = parts[0]
    args = parts[1:]

    if cmd == "cd":
        if len(args) != 1:
            raise ValueError("cd requires exactly one argument")
        new_path = change_directory(base_path, current_path, args[0])
        return new_path
    elif cmd == "ls":
        if len(args) == 1 and args[0] == "-l":
            list_directory_detailed(current_path)
        else:
            contents = list_directory(current_path)
            for item in contents:
                print(item)
        return current_path
    elif cmd == "echo":
        echo_message(' '.join(args))
        return current_path
    elif cmd == "uniq":
        if len(args) != 1:
            raise ValueError("uniq requires exactly one argument")
        unique_lines(os.path.join(current_path, args[0]))
        return current_path
    elif cmd == "chmod":
        if len(args) != 2:
            raise ValueError("chmod requires exactly two arguments")
        change_mode(os.path.join(current_path, args[1]), args[0])
        return current_path
    elif cmd == "exit":
        exit(0)
    else:
        print(f"Unknown command: {cmd}")
        return current_path


def main():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--config", required=True, help="Path to the configuration file")

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    hostname = config.get('Settings', 'hostname')
    vfs = config.get('Settings', 'vfs')
    log = config.get('Settings', 'log')
    script = config.get('Settings', 'script')

    setup_logging(log)
    extract_path = os.path.abspath("./vfs")
    extract_vfs(vfs, extract_path)
    current_path = run_start_script(script, extract_path, extract_path)

    while True:
        try:
            # Извлечение текущей директории для отображения в приглашении
            current_dir_name = os.path.basename(current_path)
            command = input(f"{hostname}:{current_dir_name}$ ")
            log_action(log, command)
            current_path = execute_command(command, extract_path, current_path)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
