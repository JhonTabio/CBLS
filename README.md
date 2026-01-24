# Command Block Language Server - CBLS
### A language server for CBScript
**Version**: v0.1.2

CBLS provides developers with a set of language features to improve the experience of coding in `cbscript`, a command scripting language created by SethBling.

This project aims to deliver community-driven tooling to support and enhance `cbscript` development.

CBLS is currently implemented in **Python** as an initial exploration of the Language Server Protocol, with a **future rewrite in Java**

![CBLS](https://github.com/user-attachments/assets/8f1ddc00-2840-4926-9086-4b95cb444c55)

## Features
These are the features I'd like to have implemented, with its current progression

- ✅ **Tokenizing documents**
- ✅ **Syntax highlighting**
- ⏳ **Parsing rules**
- ⏳  **Syntax checking**
- ⏳ **Autocomplete**
- ❌ **Find references**
- ❌ **Hover support**
- ⏳ **Diagnostics/Warnings**
- ❌ **Customizable configuration**

## Installation

> Note: CBLS is in early development and is not yet distributed as a packaged release.

### Clone the repository:
```
git clone https://github.com/JhonTabio/CBLS.git
cd CBLS
```

### Python environment (recommended)
Create a virtual environment:
```
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies:
```
pip install -r requirements.txt
```

## Usage
Start the language server:
```
python cbls.py
```

CBLS communicates over **stdio** and is intended to be launched by an LSP-compatible editor or client

## Editor Support
CBLS is designed to work with any editor that supports the Language Server Protocol

### Tested / planned integrations:
- Neovim (via nvim-lspconfig)
- VS Code (custom LSP client)
Editor-specific instructions will be added as support matures

## Related Projects

- [cbscript](https://github.com/SethBling/cbscript) – Official repository for SethBling's cbscript.

## Contributing
Contributions are always welcomed, this is my first in-depth project in making an LSP, let alone both a lexer and parser.

If you encounter bugs, see areas which can be improved, or have suggestions for new features, please feel free to open an issue or submit a pull request.
