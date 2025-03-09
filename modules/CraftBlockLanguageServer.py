from typing import Dict, List
from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range
from pygls.server import LanguageServer
from pygls.workspace import TextDocument
from modules.TokenUtils import TOKEN_MAPPING, TOKEN_TYPES

class CraftBlockLanguageServer(LanguageServer):
    """
        CraftBlockScript Language Server

        Currently able to highlight keywords and detect '#' tokens
    """

    def __init__(self, lexer, parser, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lexer = lexer
        self.parser = parser

        self.tokens: Dict[str, List[int]] = {}


    def lex(self, document: TextDocument):
        """
            Extract tokens from a given document
        """

        data = []

        prev_line = 0
        prev_column = 0

        self.lexer.lexer.input(document.source)

        while True:
            token = self.lexer.lexer.token()

            if not token:
                 break

            if (token_type := TOKEN_MAPPING.get(token.type, None)) is None:
                if token.value not in self.lexer.reserved:
                     continue
                else:
                    token_type = "keyword"

            line = token.lineno - 1
            column = self.lexer.find_column(document.source, token) - 1

            # LSP uses relative positioning
            delta_line = line - prev_line
            delta_column = column - prev_column if delta_line == 0 else column

            data.extend([delta_line, delta_column, len(token.value), TOKEN_TYPES.index(token_type), 0])

            prev_line = line
            prev_column = column

        self.tokens[document.uri] = data
        self.lexer.reset()

    def parse(self, document: TextDocument):
        """
            Extract syntactical meaning from a given document
        """

        self.parser.parse(document.source)

        diagnostics: list[Diagnostic] = []

        for d in self.parser.diagnostics:
            diag = Diagnostic(
                    range=Range(start=Position(d.lineno, d.col), end=Position(d.lineno, d.col + len(d.token.value))), 
                    message=d.message, 
                    severity=DiagnosticSeverity.Error, 
                    source="cbls")

            diagnostics.append(diag)
        
        self.publish_diagnostics(document.uri, diagnostics)
