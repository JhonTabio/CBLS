from pygls.server import LanguageServer
from lsprotocol.types import (
    CompletionItem, CompletionParams, CompletionOptions,
    Diagnostic, DiagnosticSeverity,
    DidChangeTextDocumentParams, DidOpenTextDocumentParams,
    Position, Range,
    TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_CHANGE,
    )

server = LanguageServer("cbls", "v0.1")

@server.feature(
    TEXT_DOCUMENT_COMPLETION,
    CompletionOptions(trigger_characters=["."]),
)
def completion(p: CompletionParams):
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
