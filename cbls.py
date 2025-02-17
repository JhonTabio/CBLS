from functools import reduce
from lsprotocol.types import (
    CompletionItem, CompletionParams, CompletionOptions,
    Diagnostic, DiagnosticSeverity,
    DidChangeTextDocumentParams, DidOpenTextDocumentParams,
    Position, Range, SemanticTokensRegistrationOptions,
    SemanticTokens, SemanticTokensLegend, SemanticTokensParams, 
    TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_OPEN, 
    TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL
    )
from modules.CraftBlockLanguageServer import CraftBlockLanguageServer
from modules.TokenUtils import TokenModifier, TOKEN_TYPES
from operator import or_

server = CraftBlockLanguageServer("cbls", "v0.1")

legend = SemanticTokensLegend(token_types=TOKEN_TYPES, token_modifiers=[m.name for m in TokenModifier if m.name is not None])

@server.feature(TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, SemanticTokensRegistrationOptions(legend=legend, full=True))
async def semantic_tokens(s: CraftBlockLanguageServer, p: SemanticTokensParams) -> SemanticTokens:
    """
        Provides semantic token coloring for syntax highlighting
    """

    data = []
    tokens = s.tokens.get(p.text_document.uri, [])

    for token in tokens:
        data.extend(
            [
                token.line,
                token.offset,
                len(token.text),
                TOKEN_TYPES.index(token.token_type),
                reduce(or_, token.token_modifiers, 0),
            ]
        )

    return SemanticTokens(data=data)

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
async def did_open(s: CraftBlockLanguageServer, p: DidOpenTextDocumentParams):
    """
        Handles text when document is opened in the editor
    """
    document = s.workspace.get_text_document(p.text_document.uri)
    s.parse(document)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(s: CraftBlockLanguageServer, p: DidChangeTextDocumentParams):
    """
        Handles live text changes in the editor

        This function is triggered whenever a document is modified
    """

    uri = p.text_document.uri
    document = s.workspace.get_text_document(uri)
    text = document.source # To retrieve full document
    #text = p.content_changes[0].text # To retireve what was changed
    lines = text.split('\n')

    s.parse(document)

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
