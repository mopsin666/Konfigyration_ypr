import unittest
from commands import ls, cd, chmod, echo, uniq
import os
import tempfile

class TestShellCommands(unittest.TestCase):

    def setUp(self):
        # Создаем временную директорию для тестирования
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Удаляем временную директорию
        os.rmdir(self.test_dir)

    def test_ls(self):
        # Проверим команду 'ls'
        os.mkdir(os.path.join(self.test_dir, 'test_folder'))
        result = ls(self.test_dir)
        self.assertIn('test_folder', result)

    def test_cd(self):
        # Проверим команду 'cd'
        new_dir = os.path.join(self.test_dir, 'test_folder')
        os.mkdir(new_dir)
        result = cd('test_folder', self.test_dir)
        self.assertEqual(result, new_dir)

    def test_chmod(self):
        # Проверим команду 'chmod'
        file_path = os.path.join(self.test_dir, 'test_file.txt')
        with open(file_path, 'w') as f:
            f.write('Hello, world!')
        result = chmod(file_path, 0o777)
        self.assertIn('permissions changed', result)

    def test_echo(self):
        # Проверим команду 'echo'
        result = echo('Hello, world!')
        self.assertEqual(result, 'Hello, world!')

    def test_uniq(self):
        # Проверим команду 'uniq'
        file_path = os.path.join(self.test_dir, 'test_file.txt')
        with open(file_path, 'w') as f:
            f.write('line 1\nline 2\nline 1\n')
        result = uniq(file_path)
        self.assertEqual(result, 'line 1\nline 2\n')

if __name__ == '__main__':
    unittest.main()
