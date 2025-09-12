import unittest
from unittest.mock import patch, mock_open
from frontmatters.commands.add_description import process_single_file
from pathlib import Path

class TestAddDescription(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="---\ntitle: Test\n---\n# Hello")
    @patch("frontmatters.commands.add_description.get_description", return_value="Test description")
    def test_process_single_file(self, mock_get_description, mock_open):
        process_single_file(Path("test.md"), "fake_api_key", False, "test_model")
        mock_open.assert_called_with(Path('test.md'), 'w', encoding='utf-8')
        handle = mock_open()
        handle.write.assert_called_once()
        args, kwargs = handle.write.call_args
        self.assertIn("description: Test description", args[0])

if __name__ == "__main__":
    unittest.main()