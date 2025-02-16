#from dotenv import load_dotenv
from os import getenv
from pygls.server import LanguageServer
from lsprotocol.types import (
    CompletionItem, CompletionParams, CompletionOptions,
    Diagnostic, DiagnosticSeverity,
    DidChangeTextDocumentParams, DidOpenTextDocumentParams,
    Position, Range, SemanticTokensRegistrationOptions,
    SemanticTokens, SemanticTokensLegend, SemanticTokensParams, 
    TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_OPEN, 
    TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL
    )

"""
load_dotenv()

scriptlex_path = getenv("SCRIPTLEX_PATH")

if scriptlex_path:
    from sys import path
    path.insert(1, scriptlex_path)

import scriptlex
print(scriptlex.keywords)
"""

class CraftBlockLanguageServer(LanguageServer):
    """
        CraftBlockScript Language Server

        Currently able to highlight keywords and detect '#' tokens
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

server = LanguageServer("cbls", "v0.1")

TOKEN_TYPES = [
    "keyword",
    "function",
    "variable",
    "class",
    "string"
]

TOKEN_MODIFIERS = [
    "declaration",
    "readonly",
    "static"
]

KEYWORDS = [
    "if", 
    "while", 
    "return", 
    "for", 
    "def", 
    "class"
]

legend = SemanticTokensLegend(token_types=TOKEN_TYPES, token_modifiers=TOKEN_MODIFIERS)

@server.feature(TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, SemanticTokensRegistrationOptions(legend=legend, full=True))
async def semantic_tokens(s: LanguageServer, p: SemanticTokensParams) -> SemanticTokens:
    """
        Provides semantic token coloring for syntax highlighting
    """

    uri = p.text_document.uri
    text = s.workspace.get_text_document(uri).source
    lines = text.split('\n')

    tokens = []

    for i, line in enumerate(lines):
        words = line.split()

        for word in words:
            start = line.find(word)
            length = len(word)

            if start == -1:
                continue
            
            # Keyword
            if word in KEYWORDS:
                tokens.extend([i, start, length, 0, 0])
                s.show_message(f"Found {word} at ({start},{length}) line {i}")
            # String
            elif word.startswith('"') and word.endswith('"'):
                tokens.extend([i, start, length, 1, 0])

    return SemanticTokens(data=tokens)

@server.feature(
    TEXT_DOCUMENT_COMPLETION,
    CompletionOptions(trigger_characters=["."]),
)
def completion(p: CompletionParams) -> list[CompletionItem]:
    """
        Handles autocomplete suggestions
    """
    document = server.workspace.get_text_document(p.text_document.uri)
    current_line = document.lines[p.position.line].strip()

    if not current_line.endswith("hello."):
        return []

    return [
        CompletionItem(label="world"),
        CompletionItem(label="friend"),
        CompletionItem(label="mate"),
    ]

@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(s: LanguageServer, p: DidOpenTextDocumentParams):
    """
        Handles text when document is opened in the editor
    """
    s.show_message("This did, in fact, open")

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(s: LanguageServer, p: DidChangeTextDocumentParams):
    """
        Handles live text changes in the editor

        This function is triggered whenever a document is modified
    """

    uri = p.text_document.uri
    text = s.workspace.get_text_document(uri).source # To retrieve full document
    #text = p.content_changes[0].text # To retireve what was changed
    lines = text.split('\n')

    diagnostics = []

    for i, line in enumerate(lines):
        if '#' not in line:
         continue
        
        index = line.rindex('#')
        d = Diagnostic(
                range=Range(start=Position(i, index), end=Position(i, len(line))), 
                message=f"Found '#' in pos {index} in line {i + 1}", 
                severity=DiagnosticSeverity.Warning, 
                source="cbls")
        diagnostics.append(d)
    
    s.publish_diagnostics(uri, diagnostics)


if __name__ == "__main__":
    server.start_io()
