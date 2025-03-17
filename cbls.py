from lsprotocol.types import (
    CompletionItem, CompletionParams, CompletionOptions,
    DidChangeTextDocumentParams, DidOpenTextDocumentParams,
    SemanticTokensRegistrationOptions, SemanticTokens,
    SemanticTokensLegend, SemanticTokensParams, 
    TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_OPEN, 
    TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL
    )
from modules.CommandBlockLanguageServer import CommandBlockLanguageServer
from modules.CommandBlockLexer import CBLex
from modules.CommandBlockParser import CBParse
from modules.TokenUtils import TokenModifier, TOKEN_TYPES

lexer = CBLex()
parser = CBParse(lexer)
server = CommandBlockLanguageServer(lexer, parser, "cbls", "v0.1.1")

legend = SemanticTokensLegend(token_types=TOKEN_TYPES, token_modifiers=[m.name for m in TokenModifier if m.name is not None])

@server.feature(TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, SemanticTokensRegistrationOptions(legend=legend, full=True))
async def semantic_tokens(s: CommandBlockLanguageServer, p: SemanticTokensParams) -> SemanticTokens:
    """
        Provides semantic token coloring for syntax highlighting
    """
    return SemanticTokens(data=s.tokens.get(p.text_document.uri, []))

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
async def did_open(s: CommandBlockLanguageServer, p: DidOpenTextDocumentParams):
    """
        Handles text when document is opened in the editor
    """
    document = s.workspace.get_text_document(p.text_document.uri)
    s.lex(document)
    s.parse(document)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(s: CommandBlockLanguageServer, p: DidChangeTextDocumentParams):
    """
        Handles live text changes in the editor

        This function is triggered whenever a document is modified
    """

    uri = p.text_document.uri
    document = s.workspace.get_text_document(uri)
    text = document.source # To retrieve full document
    #text = p.content_changes[0].text # To retireve what was changed
    #lines = text.split('\n')

    s.lex(document)
    s.parse(document)

if __name__ == "__main__":
    server.start_io()
