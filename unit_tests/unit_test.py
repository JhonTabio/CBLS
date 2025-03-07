from modules.cblex import CBLex
from modules.cbparse import CBParse

parser = CBParse(CBLex())

test = """Unkown_ID

Second_Unkown_ID

dir "unit_test.py"
"""

parser.parse(test)
parser.reset()
