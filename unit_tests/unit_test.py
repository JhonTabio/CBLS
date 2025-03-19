import unittest
from modules.CommandBlockLexer import CBLex
from modules.CommandBlockParser import CBParse
from typing import List, Optional

class CBLS_Tests(unittest.TestCase):
    # unittest calls 'setUpClass' once prior to any testing
    @classmethod
    def setUpClass(cls) -> None:
        # PLY Parsers *should* be defined once
        cls.parser = CBParse(CBLex())

    # unittest calls 'tearDown' after a testcase
    def tearDown(self) -> None:
        self.parser.reset()

    # Helper function to test results
    def parser_test(self, input_data: str, expected_errors: List[str], file_ext: Optional[str] = None) -> None:
        ext, _ = self.parser.parse(input_data)
    
        if file_ext:
            self.assertEqual(ext, file_ext)

        query = [d.message for d in self.parser.diagnostics]
        self.assertEqual(query, expected_errors)

    ### Unit tests
    ## New file testing
    # Empty file
    def test_empty_file(self) -> None:
        """
            Empty files will be processed as a library file.
            This is because library files have no start of file restriction, unlike script files.
        """
        input_data = ""
        expected_errors = []
        ext = "cblib"

        self.parser_test(input_data, expected_errors, ext)

    # Proper CBScript start
    def test_cbscript_start_file(self) -> None:
        input_data = """dir 'CommandBlockLanguageServer Unit Testing :)'"""
        expected_errors = []
        ext = "cbscript"
        
        self.parser_test(input_data, expected_errors, ext)


    # Improper CBScript start
    def test_cbscript_improper_start_file(self) -> None:
        input_data = """
        dir 'CommandBlockLanguageServer Unit Testing :|'"""
        expected_errors = ["Syntax error at line 0. Unexpected start of file token, please ensure 'DIR' is at the top"]
        ext = "cbscript"
        
        self.parser_test(input_data, expected_errors, ext)


    # Error CBScript start
    def test_cbscript_error_start_file(self) -> None:
        input_data = """Unknown_ID
        dir 'CommandBlockLanguageServer Unit Testing :|'"""
        expected_errors = [
            "Syntax error at line 1 column 1. Unexpected ID symbol 'Unknown_ID' in state 0. Expected ['DIR', 'NEWLINE', 'ADVANCEMENT', 'ARRAY', 'DOLLAR', 'IMPORT', 'ITEM_MODIFIER', 'LOOT_TABLE', 'ATID', 'DEFINE', 'PREDICATE', 'RESET', 'CLOCK', 'FUNCTION', 'MACRO', '$end']",
            "Syntax error at line 0. Unexpected start of file token, please ensure 'DIR' is at the top"
        ]
        ext = "cbscript"
        
        self.parser_test(input_data, expected_errors, ext)

    # Proper CBLib start
    def test_cblib_start_file(self) -> None:
        input_data = "import unittest"
        expected_errors = []
        ext = "cblib"
        
        self.parser_test(input_data, expected_errors, ext)


if __name__ == "__main__":
    unittest.main()
