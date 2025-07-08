import unittest
import os
import io
from functions.last_lines import last_lines


class TestLastLines(unittest.TestCase):

    def setUp(self):
        self.test_dir = "tests/test_files"
        os.makedirs(self.test_dir, exist_ok=True)

    def _create_file(self, filename, content, mode='w'):
        filepath = os.path.join(self.test_dir, filename)
        if 'b' in mode:
            with open(filepath, mode) as f:
                f.write(content)
        else:
            with open(filepath, mode, encoding='utf-8') as f:
                f.write(content)
        return filepath

    def test_empty_file(self):
        filepath = self._create_file("empty.txt", "")
        self.assertEqual(list(last_lines(filepath)), [])

    def test_single_line_file(self):
        filepath = self._create_file("single_line.txt", "Single line file.\n")
        self.assertEqual(list(last_lines(filepath)), ["Single line file.\n"])

    def test_multiple_lines_file(self):
        content = "Line 1\nLine 2\nLine 3\n"
        filepath = self._create_file("multiple_lines.txt", content)
        expected = ["Line 3\n", "Line 2\n", "Line 1\n"]
        self.assertEqual(list(last_lines(filepath)), expected)

    def test_file_without_trailing_newline(self):
        content = "First line\nSecond line\nThird line no newline."
        filepath = self._create_file("no_trailing_newline.txt", content)
        expected = ["Third line no newline.\n", "Second line\n", "First line\n"]
        self.assertEqual(list(last_lines(filepath)), expected)

    def test_windows_line_endings(self):
        content = "Line 1\r\nLine 2\r\nLine 3\r\n".encode('utf-8') # encode para 'wb' mode
        filepath = self._create_file("windows_lines.txt", content, mode='wb')
        expected = ["Line 3\n", "Line 2\n", "Line 1\n"]
        result = [line for line in last_lines(filepath)]
        self.assertEqual(result, expected)

    def test_mixed_line_endings(self):
        content = "Line 1\nLine 2\r\nLine 3\n".encode('utf-8')
        filepath = self._create_file("mixed_lines.txt", content, mode='wb')
        expected = ["Line 3\n", "Line 2\n", "Line 1\n"]
        result = [line for line in last_lines(filepath)]
        self.assertEqual(result, expected)

    def test_large_file_with_buffer_size(self):
        long_line = "Long line to test buffer size." * 50 + "\n"
        content = ""
        for i in range(100): # 100 linhas
            content += f"Line {i+1}: {long_line}"
        
        filepath = self._create_file("large_file.txt", content)

        expected = []
        for i in range(99, -1, -1):
            expected.append(f"Line {i+1}: {long_line}")

        # Teste com o default buffer size
        self.assertEqual(list(last_lines(filepath)), expected)
        
        # Teste com buffer size pequeno
        self.assertEqual(list(last_lines(filepath, buffer_size=10)), expected)
        
        # Teste com buffer size maior que o tamanho do arquivo
        self.assertEqual(list(last_lines(filepath, buffer_size=len(content.encode('utf-8')) + 100)), expected)

    def test_file_with_non_ascii_characters(self):
        content = "áéíóú\n你好！\n"
        filepath = self._create_file("unicode_file.txt", content)
        expected = ["你好！\n", "áéíóú\n"]
        self.assertEqual(list(last_lines(filepath)), expected)

    def test_file_with_emojis_bigger_than_buffer(self):
        content = "👩🏾‍🦳\n👩🏾‍🦳👩🏾‍🦳\n" #12 bytes emoji
        filepath = self._create_file("emoji_file.txt", content)
        expected = ["👩🏾‍🦳👩🏾‍🦳\n", "👩🏾‍🦳\n"]
        self.assertEqual(list(last_lines(filepath, 1)), expected)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            list(last_lines("non_existent_file.txt"))

    def tearDown(self):
        """Deleta os arquivos de teste"""
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)


if __name__ == '__main__':
    unittest.main()
