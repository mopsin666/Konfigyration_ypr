import csv
import os
import unittest
import zipfile
from io import StringIO
from unittest.mock import patch

from main import parse_args, open_filesystem, log_action, execute_command, zip_fs


class TestShellEmulator(unittest.TestCase):
    test_log_file = None
    zip_path = None

    @classmethod
    def setUpClass(cls):
        cls.test_log_file = 'test_log.csv'

        # Создание zip-файла для теста
        cls.zip_path = 'test_fs.zip'
        with zipfile.ZipFile(cls.zip_path, 'w') as zipf:
            zipf.writestr('file1.txt', 'Hello World')
            zipf.writestr('dir1/', '')

    @classmethod
    def tearDownClass(cls):
        # Закрываем файловую систему, если она еще открыта
        if zip_fs:
            zip_fs.close()

        # Удаление временных файлов после завершения всех тестов
        if os.path.exists(cls.zip_path):
            os.remove(cls.zip_path)
        if os.path.exists(cls.test_log_file):
            os.remove(cls.test_log_file)

    def setUp(self):
        # Открываем файловую систему перед каждым тестом
        open_filesystem(self.zip_path)

        # Удаление лог-файла перед каждым тестом
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

        # Выводим название текущего теста
        print(f"Running test: {self._testMethodName}")

    def tearDown(self):
        # Закрываем файловую систему после каждого теста
        if zip_fs:
            zip_fs.close()

        # Получаем результат теста
        result = self._outcome.result
        test_name = self._testMethodName

        # Проверяем ошибки и неудачи
        if any(err for err in result.errors if err[0] is self):
            print(f"Test {test_name}: ERROR")
        elif any(fail for fail in result.failures if fail[0] is self):
            print(f"Test {test_name}: FAILED")
        else:
            print(f"Test {test_name}: SUCCESS")

    def test_parse_args(self):
        test_args = ['--user', 'test_user', '--filesystem', self.zip_path, '--logfile', self.test_log_file]
        with patch('sys.argv', ['your_shell_emulator.py'] + test_args):
            args = parse_args()
            self.assertEqual(args.user, 'test_user')
            self.assertEqual(args.filesystem, self.zip_path)
            self.assertEqual(args.logfile, self.test_log_file)

    def test_log_action(self):
        log_action('test_user', 'test_action', self.test_log_file)
        with open(self.test_log_file, newline='') as file:
            log_content = list(csv.reader(file))
        self.assertEqual(log_content[0], ['test_user', 'test_action'])

    def test_execute_command_ls(self):
        current_directory = '/'

        with patch('sys.stdout', new=StringIO()) as fake_output:
            execute_command('ls', 'test_user', self.test_log_file, fake_output, current_directory)
            self.assertIn('file1.txt', fake_output.getvalue())  # Проверяем наличие файла

        with patch('sys.stdout', new=StringIO()) as fake_output:
            execute_command('ls dir1', 'test_user', self.test_log_file, fake_output, current_directory)
            self.assertEqual(fake_output.getvalue().strip(), '')  # Проверяем, что директория пустая

    def test_execute_command_cd(self):
        current_directory = '/'

        with patch('sys.stdout', new=StringIO()) as fake_output:
            current_directory = execute_command('cd dir1', 'test_user', self.test_log_file, fake_output,
                                                current_directory)
            self.assertEqual(os.path.normpath(current_directory),
                             os.path.normpath('/dir1'))  # Проверьте, что каталог изменился

        with patch('sys.stdout', new=StringIO()) as fake_output:
            execute_command('cd non_existent_dir', 'test_user', self.test_log_file, fake_output,
                            current_directory)
            self.assertIn('Ошибка: выход за пределы виртуальной ФС или такой директории нет', fake_output.getvalue())

    def test_execute_command_whoami(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            execute_command('whoami', 'test_user', self.test_log_file, fake_output, '/')
            self.assertIn('test_user', fake_output.getvalue())

    def test_execute_command_chmod(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            execute_command('chmod 755 file1.txt', 'test_user', self.test_log_file, fake_output, '/')
            self.assertIn('755', fake_output.getvalue())

        with patch('sys.stdout', new=StringIO()) as fake_output:
            execute_command('chmod 755', 'test_user', self.test_log_file, fake_output, '/')
            self.assertIn('Неправильная команда chmod', fake_output.getvalue())

    def test_execute_command_exit(self):
        with patch('builtins.exit', side_effect=SystemExit) as mock_exit:
            with self.assertRaises(SystemExit):  # Проверяем, что вызвано исключение SystemExit
                execute_command('exit', 'test_user', self.test_log_file, None, '/')
            mock_exit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
