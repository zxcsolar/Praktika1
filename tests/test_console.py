import os
import unittest

from src.console import env_var
from src.console import parse_command


class TestConsole(unittest.TestCase):

    def test_parse_command(self):
        result = parse_command("ls -l /home")
        self.assertEqual(result, ["ls", "-l", "/home"])

    def test_parse_quotes(self):
        result = parse_command('cd "my folder"')
        self.assertEqual(result, ["cd", "my folder"])

    def test_env_var(self):
        os.environ["TEST_VAR"] = "test_value"
        result = env_var("$TEST_VAR")
        self.assertEqual(result, "test_value")


if __name__ == "__main__":
    unittest.main()