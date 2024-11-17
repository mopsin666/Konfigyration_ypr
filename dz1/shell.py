import os
import logging
from commands import ls, cd, chmod, echo, uniq
from filesystem import VFS

class Shell:
    def __init__(self, vfs_path, log_path, script_path):
        self.vfs = VFS(vfs_path)
        self.current_directory = "/"
        self.hostname = "localhost"
        self.log_path = log_path
        self.script_path = script_path
        self.commands = {
            'ls': ls,
            'cd': cd,
            'chmod': chmod,
            'echo': echo,
            'uniq': uniq
        }

    def run(self):
        self._load_script()
        while True:
            command = input(f"{self.hostname}:{self.current_directory}$ ")
            if command == "exit":
                break
            self._execute_command(command)

    def _load_script(self):
        # Загружаем команды из стартового скрипта, если он существует.
        if os.path.exists(self.script_path):
            with open(self.script_path, 'r') as script:
                for line in script.readlines():
                    self._execute_command(line.strip())

    def _execute_command(self, command):
        try:
            parts = command.split()
            cmd = parts[0]
            args = parts[1:]
            if cmd in self.commands:
                result = self.commands[cmd](*args, current_directory=self.current_directory)
                self._log_command(command, result)
                print(result)
            else:
                print(f"{cmd}: command not found")
        except Exception as e:
            print(f"Error: {e}")

    def _log_command(self, command, result):
        logging.basicConfig(filename=self.log_path, level=logging.INFO)
        logging.info(f"Command: {command} - Result: {result}")
