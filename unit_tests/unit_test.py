import unittest
from modules.CommandBlockLexer import CBLex
from modules.CommandBlockParser import CBParse
from typing import List, Optional

class unit_test(unittest.TestCase):
    # unittest calls 'setUp' prior to any testing
    def setUp(self) -> None:
        self.parser = CBParse(CBLex())

    # unittest calls 'tearDown' after a testcase
    def tearDown(self) -> None:
        self.parser.reset()

    # Helper function to test results
    def error_test(self, input_data: str, expected: List[str], file_ext: Optional[str] = None) -> None:
        ext, _ = self.parser.parse(input_data)
    
        if file_ext:
            self.assertEqual(ext, file_ext)

        query = [d.message for d in self.parser.diagnostics]
        self.assertEqual(query, expected)

    ### Unit tests
    ## New file testing
    # Empty file
    def test_empty_file(self) -> None:
        """
            Empty files will be processed as a library file.
            This is because library files have no start of file restriction, unlike script files.
        """
        input_data = ""
        expected = []
        ext = "cblib"

        self.error_test(input_data, expected, ext)

if __name__ == "__main__":
    unittest.main()
