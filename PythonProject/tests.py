import unittest
import os
import shutil
import emulator


class TestEmulator(unittest.TestCase):

    def setUp(self):
        self.vfs_path = "./vfs"
        if os.path.exists(self.vfs_path):
            shutil.rmtree(self.vfs_path)
        os.makedirs(self.vfs_path)
        with open(os.path.join(self.vfs_path, "test.txt"), 'w') as f:
            f.write("line1\nline2\nline1\nline3\n")
        emulator.setup_logging("log.xml")

    def tearDown(self):
        if os.path.exists(self.vfs_path):
            shutil.rmtree(self.vfs_path)

    def test_cd(self):
        current_path = self.vfs_path
        new_path = emulator.change_directory(current_path, "test_dir")
        self.assertEqual(new_path, os.path.join(current_path, "test_dir"))

    def test_ls(self):
        contents = emulator.list_directory(self.vfs_path)
        self.assertIn("test.txt", contents)

    def test_echo(self):
        message = "Hello, World!"
        output = emulator.echo_message(message)
        self.assertEqual(output, message)

    def test_uniq(self):
        file_path = os.path.join(self.vfs_path, "test.txt")
        unique_lines = emulator.unique_lines(file_path)
        expected_lines = ["line1\n", "line2\n", "line3\n"]
        self.assertEqual(unique_lines, expected_lines)

    def test_chmod(self):
        file_path = os.path.join(self.vfs_path, "test.txt")
        emulator.change_mode(file_path, "0777")
        mode = oct(os.stat(file_path).st_mode & 0o777)
        self.assertEqual(mode, "0o777")


if __name__ == "__main__":
    unittest.main()
