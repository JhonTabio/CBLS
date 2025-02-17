from typing import Dict, List
from pygls.server import LanguageServer
from pygls.workspace import TextDocument
from modules.TokenUtils import (
        KEYWORDS,
        Token, 
        IDENTIFIERS, SPACE)

class CraftBlockLanguageServer(LanguageServer):
    """
        CraftBlockScript Language Server

        Currently able to highlight keywords and detect '#' tokens
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tokens: Dict[str, List[Token]] = {}


    def lex(self, document: TextDocument) -> List[Token]:
        """
            Extract tokens from a given document
        """

        res = []

        prev_line, prev_offset = 0, 0

        for i, line in enumerate(document.lines):
            prev_offset = current_offset = 0
            remaining = len(line)

            while line:
                if (match := SPACE.match(line)) is not None: # Skip whitespaces
                    current_offset += len(match.group(0))
                    line = line[match.end():]

                elif (match := IDENTIFIERS.match(line)) is not None:
                    identified_text = match.group(0)

                    res.append(
                        Token(
                            line=i - prev_line,
                            offset = current_offset - prev_offset,
                            text=identified_text
                            )
                        )

                    line = line[match.end():]
                    prev_offset = current_offset
                    prev_line = i
                    current_offset += len(identified_text)

                else:
                    raise RuntimeError(f"Could not match {line!r}")

                if (n := len(line)) == remaining:
                    raise RuntimeError("Managed our way to an infinite loop")
                else:
                    remaining = n
        return res

    def process_tokens(self, tokens: List[Token]):
        """
            Process all of our tokens, provide modifier context
        """
        def prev(idx):
            """Get the previous token, if possible"""
            if idx < 0:
                return None

            return tokens[idx - 1]

        def next(idx):
            """Get the next token, if possible"""
            if idx >= len(tokens) - 1:
                return None

            return tokens[idx + 1]

        for idx, token in enumerate(tokens):
            if token.text in KEYWORDS:
                token.token_type = "keyword"
            else:
                token.token_type = "variable"

    def parse(self, document: TextDocument):
        """
            Parse a given document, extracting and retrieving context for 
            tokens and storing them
        """
        tokens = self.lex(document)
        self.process_tokens(tokens)
        self.tokens[document.uri] = tokens

