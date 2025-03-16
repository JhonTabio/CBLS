import ply.yacc as yacc

class CBDiagnostic(object):
    def __init__(self, token, col, state, expected, message=None):
        self.token = token
        self.lineno = token.lineno - 1
        self.col = col - 1
        self.state = state
        self.message = f"Syntax error at line {token.lineno} column {col}. Unexpected {token.type} symbol {repr(token.value)} in state {state}. Expected {expected}" if message is None else message
        self.label = ""

    def __str__(self):
        return self.message + "\n" + self.label

class CBParse(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.file_params = ["scale"]

        self.data = None
        self.diagnostics: list[CBDiagnostic] = []

        self.executee = {
            "attacker",
            "controller",
            "leasher",
            "origin",
            "owner",
            "passengers",
            "target",
            "vehicle"
        }

        self.axis = {"x", "y", "z", "xy", "xz", "yz", "xyz"}

    ### Parser rules
    ## File type rules -- Top level rules
    # .cbscript files
    def p_cbscript(self, p):
        """cbscript : script"""
        p[0] = ("cbscript", p[1])

    #def p_cblib(self, p):
        #"""cblib : lib"""
        #p[0] = ("cblib", p[1])

    ## Program type rules
    # Script rules
    def p_script(self, p):
        """script : dir optdesc file_params top_level_blocks"""
        p[0] = {
            "DIR": p[1],
            "DESC": p[2]
        }

    # Dir rules
    def p_dir(self, p):
        """dir : DIR string newlines"""
        p[0] = p[2]

    def p_dir_error(self, p):
        """dir : DIR error newlines"""
        p[0] = "No output directroy"
        self.diagnostics[-1].label = "Expected a string for dir"
        self.parser.errok()

    # Desc rules
    def p_optdesc(self, p):
        """optdesc : DESC string newlines
                    | empty"""
        if len(p) < 4:
            p[0] = "No Description"
        else:
            p[0] = p[2]

    def p_optdesc_error(self, p):
        """optdesc : DESC error newlines"""
        p[0] = "No Description"
        self.diagnostics[-1].label = "Expected a string for desc"
        self.parser.errok()

    # File param rules
    def p_file_params(self, p):
        """file_params : file_param file_params optnewlines
                        | empty"""
        if len(p) > 2:
            n, v = p[1]
            p[2][n] = v
            p[0] = p[2]
        else:
            p[0] = {}

    def p_file_param(self, p):
        """file_param : ID int newlines"""
        if p[1] not in self.file_params:
            print(f"File param error: Unknown parameter '{p[1]}' at line {p.lineno(1)}")
        p[0] = (p[1], int(p[2]))

    def p_file_param_error(self, p):
        """file_param : ID error newlines"""
        if p[1] not in self.file_params:
            print(f"File param error: Unknown parameter '{p[1]}' at line {p.lineno(1)}")
        p[0] = (p[1], int(1000))
        self.parser.errok()

    ## Top level rules
    # Top level block rule
    def p_top_level_block(self, p):
        """top_level_block : advancement
                            | array
                            | const_assign optnewlines
                            | import
                            | item_modifier
                            | loot_table
                            | selector_assign
                            | selector_define_block
                            | sections
                            | predicate"""

    def p_top_level_blocks(self, p):
        """top_level_blocks : top_level_block top_level_blocks optnewlines
                            | empty"""

    def p_import(self, p):
        """import : IMPORT ID optnewlines"""

    ## Section rules
    def p_sections(self, p):
        """sections : section sections optnewlines
                    | empty"""

    # Section rule
    def p_section(self, p):
        """section : reset_section
                    | clock_section
                    | function_section optnewlines
                    | macro_section"""
        p[0] = p[1]

    # Reset rule - Entry point
    def p_reset_section(self, p):
        """reset_section : RESET newlines code_blocks END newlines"""
        pass

    def p_reset_section_error(self, p):
        """reset_section : RESET error END newlines"""
        self.parser.errok()
        pass

    # Clock rule - Update point
    def p_clock_section(self, p):
        """clock_section : CLOCK ID newlines code_blocks END newlines"""

    def p_clock_section_error(self, p):
        """clock_section : CLOCK error END newlines"""
        self.parser.errok()

    # Function rule
    def p_function_section(self, p):
        """function_section : FUNCTION FUNCTION_ID id_list RPAREN newlines code_blocks END"""

    def p_function_section_error(self, p):
        """function_section : FUNCTION error END"""
        self.parser.errok()

    def p_id_list(self, p):
        """id_list : ID COMMA id_list
                    | ID
                    | empty"""

    def p_function_call(self, p):
        """function_call : ID COLON FUNCTION_ID expr_list RPAREN opt_with_macro
                            | FUNCTION_ID expr_list RPAREN opt_with_macro"""

    def p_function_call_block(self, p):
        """function_call_block : with function_call
                                | function_call"""

    def p_method_call(self, p):
        """method_call : full_selector DOT FUNCTION_ID expr_list RPAREN opt_with_macro"""

    def p_method_call_block(self, p):
        """method_call_block : with method_call
                                | method_call"""

    ## Code block rules
    def p_code_blocks(self, p):
        """code_blocks : code_block code_blocks optnewlines
                        | empty"""

    # Command code block rule
    def p_command_code_block(self, p):
        """code_block : COMMAND optnewlines"""
        # TODO: Validate command

    def p_move_code_block(self, p):
        """code_block : MOVE full_selector rel_coords optnewlines"""

    def p_assignment_code_block(self, p):
        """code_block : assign optnewlines"""

    def p_constant_assignment_code_block(self, p):
        """code_block : const_assign optnewlines"""

    def p_create_code_block(self, p):
        """code_block : variable EQUALS create_block optnewlines
                        | create_block optnewlines"""

    def p_define_name_code_block(self, p):
        """code_block : DEFINE NAME ID EQUALS string optnewlines"""

    def p_selector_block_code_block(self, p):
        """code_block : selector_assign optnewlines
                        | selector_define_block optnewlines"""

    def p_function_call_code_block(self, p):
        """code_block : function_call_block optnewlines
                        | method_call_block optnewlines
                        | macro_call optnewlines
                        | with_anon optnewlines"""

    ## Execute rules
    # Execute items
    def p_execute_items(self, p):
        """execute_items : execute_item execute_items
                            | empty"""

    # Execute item
    def p_execute_item(self, p):
        """execute_item : IF conditionals
                        | UNLESS conditionals
                        | AS full_selector
                        | AT full_selector opt_anchor
                        | AT full_selector opt_anchor rel_coords
                        | AT opt_anchor rel_coords
                        | AT vector_expr
                        | AT LPAREN const_value RPAREN vector_expr
                        | IN OVERWORLD
                        | IN THE_NETHER
                        | IN THE_END"""

    def p_execute_on(self, p):
        """execute_item : ON ID"""

        if p[2] not in self.executee:
            self.diagnostics.append(CBDiagnostic(p.slice[2], self.lexer.find_column(self.data, p.slice[2]), self.parser.state, self.executee))

    def p_execute_rotated(self, p):
        """execute_item : ROTATED full_selector"""

    def p_execute_facing_entity(self, p):
        """execute_item : FACING full_selector"""

    def p_execute_facing_relative_coordinates(self, p):
        """execute_item : FACING rel_coords"""

    def p_execute_align(self, p):
        """execute_item : ALIGN ID"""

        if p[2] not in self.axis:
            self.diagnostics.append(CBDiagnostic(p.slice[2], self.lexer.find_column(self.data, p.slice[2]), self.parser.state, self.executee))

    # Anchor rule
    def p_anchor(self, p):
        """opt_anchor : EYES
                        | FEET
                        | empty"""

    def p_optional_constant_value(self, p):
        """opt_const_value : const_value
                            | empty"""

    def p_local_coordinates(self, p):
        """local_coord : POWER opt_const_value"""

    def p_relative_coordinate(self, p):
        """rel_coord : const_value
                        | POWER const_value
                        | TILDE const_value
                        | TILDE
                        | TILDE_EMPTY"""

    def p_relative_coordinates(self, p):
        """rel_coords : rel_coord rel_coord rel_coord
                        | local_coord local_coord local_coord"""

    def p_optional_coordinates(self, p):
        """opt_coords : AT rel_coords
                        | empty"""

    def p_execute_else_list(self, p):
        """else_list : else_item else_list
                        | empty"""

    # Execute else rule
    def p_execute_else_item(self, p):
        """else_item : ELSE execute_items newlines code_blocks
                        | ELSE newlines code_blocks"""

    def p_execute_chain(self, p):
        """code_block : execute_items newlines code_blocks else_list END optnewlines"""

    def p_execute_inline(self, p):
        """code_block : execute_items DO code_block
                        | execute_items THEN code_block"""

    # Execute if rule
    def p_executre_if(self, p):
        """code_block : IF const_value newlines code_blocks else_list END optnewlines"""

    # Execute as rule
    def p_execute_as(self, p):
        """code_block : AS variable newlines code_blocks else_list END optnewlines
                        | AS variable LPAREN ATID RPAREN newlines code_blocks else_list END optnewlines"""

    # Execute as do rule
    def p_execute_as_do(self, p):
        """code_block : AS variable DO code_block else_list optnewlines
                        | AS variable LPAREN ATID RPAREN DO code_block optnewlines"""

    # Execute as inline create
    def p_execute_as_create(self, p):
        """code_block : AS create_block newlines code_blocks else_list END optnewlines
                        | AS create_block DO code_block optnewlines"""
    ## Conditional rules
    # Conditional rule
    def p_conditional(self, p):
        """conditional : full_selector
                        | PREDICATE ID
                        | expr EQUALS_EQUALS expr
                        | expr LESS expr
                        | expr LESS_EQUALS expr
                        | expr GREATER expr
                        | expr GREATER_EQUALS expr
                        | vector_variable EQUALS_EQUALS vector_variable
                        | NOT expr
                        | expr
                        | nbt_object
                        | nbt_list"""

    def p_conditionals(self, p):
        """conditionals : conditional AND conditionals
                        | conditional"""
    
    def p_conditional_block(self, p):
        """conditional : BLOCK rel_coords const_ID opt_block_state opt_tile_data
                        | BLOCK rel_coords ID opt_block_state opt_tile_data
                        | BLOCK const_ID opt_block_state opt_tile_data
                        | BLOCK ID opt_block_state opt_tile_data"""

    def p_optional_block_state(self, p):
        """opt_block_state : LBRACKET block_states RBRACKET
                            | empty"""

    def p_block_states(self, p):
        """block_states : ID EQUALS ID COMMA block_states
                        | ID EQUALS virtual_int COMMA block_states
                        | FACING EQUALS ID COMMA block_states
                        | FACING EQUALS virtual_int COMMA block_states
                        | ID EQUALS ID
                        | ID EQUALS virtual_int
                        | FACING EQUALS ID
                        | FACING EQUALS virtual_int"""

    def p_optional_tile_data(self, p):
        """opt_tile_data : json_object
                            | empty"""

    def p_if_else(self, p):
        """code_block : IF const_value newlines code_blocks ELSE newlines code_blocks END optnewlines"""

    ## Loop rules
    # For loop rule
    def p_for(self, p):
        """code_block : FOR variable EQUALS expr TO expr BY expr newlines code_blocks END optnewlines
                        | FOR variable EQUALS expr TO expr newlines code_blocks END optnewlines
                        | FOR const_ID IN const_value newlines code_blocks END optnewlines
                        | FOR ATID IN full_selector newlines code_blocks END optnewlines"""

    # While loop rule
    def p_while(self, p):
        """code_block : WHILE conditionals newlines code_blocks END optnewlines
                        | WHILE conditionals execute_items newlines code_blocks END optnewlines"""

    ## Create rules
    # Create ATID
    def p_ATID_create(self, p):
        """create_block : CREATE ATID rel_coords
                        | CREATE ATID"""

    def p_ATID_index_create(self, p):
        """create_block : CREATE ATID LBRACKET const_value RBRACKET rel_coords
                        | CREATE ATID LBRACKET const_value RBRACKET"""

    ## Macros 
    # Macro section
    def p_macro_section(self, p):
        """macro_section : MACRO DOLLAR FUNCTION_ID macro_args newlines code_blocks END optnewlines"""

    def p_macro_args(self, p):
        """macro_args : macro_params RPAREN
                        | empty"""

    def p_macro_params(self, p):
        """macro_params : const_ID COMMA macro_params
                        | const_ID
                        | empty"""

    # With rule
    def p_with(self, p):
        """with : WITH newlines with_items"""

    def p_with_items(self, p):
        """with_items : with_item with_items
                        | with_item"""

    def p_with_item(self, p):
        """with_item : DOLLAR LPAREN ID RPAREN EQUALS expr newlines
                        | DOLLAR LPAREN ID RPAREN EQUALS string newlines"""

    def p_with_macro(self, p):
        """opt_with_macro : WITH MACROS
                            | empty"""

    def p_with_anon(self, p):
        """with_anon : with DO newlines code_blocks END optnewlines"""

    # Macro call rule
    def p_macro_call(self, p):
        """macro_call : DOLLAR FUNCTION_ID macro_call_args"""

    def p_macro_call_args(self, p):
        """macro_call_args : macro_call_params RPAREN
                            | empty"""

    def p_macro_call_params(self, p):
        """macro_call_params : macro_call_params COMMA macro_call_params
                                | macro_call_params
                                | const_value
                                | empty"""

    ## Full Selector
    # Full Selector
    def p_full_selector(self, p):
        """full_selector : ATID"""

    def p_full_selector_qualifiers(self, p):
        """full_selector : ATID LBRACKET const_int RBRACKET
                        | ATID LBRACKET qualifiers RBRACKET"""

    ## Qualifiers
    def p_qualifier_single(self, p):
        """qualifiers : qualifier
                        | empty"""

    def p_qualifier_list(self, p):
        """qualifiers : qualifiers COMMA qualifier
                        | qualifiers AND qualifier"""

    def p_qualifier_empty(self, p):
        """qualifier : ID EQUALS"""

    def p_qualifier_not(self, p):
        """qualifier : ID EQUALS NEGATION ID
                        | NOT ID"""

    def p_qualifier_id(self, p):
        """qualifier : ID"""

    def p_qualifier_builtin(self, p):
        """qualifier : ID EQUALS const_int DOT DOT const_int
                    | ID EQUALS DOT DOT const_int
                    | ID EQUALS const_int DOT DOT"""

    def p_qualifier_binop(self, p):
        """qualifier : ID EQUALS const_int
                     | ID EQUALS ID
                     | NAME EQUALS ID
                     | ID EQUALS_EQUALS const_int
                     | ID GREATER_EQUALS const_int
                     | ID LESS_EQUALS const_int
                     | ID GREATER const_int
                     | ID LESS const_int
                     | ID EQUALS json_object"""

    ## Selector rules
    def p_selector_define(self, p):
        """selector_define_block : DEFINE ATID EQUALS full_selector newlines selector_definition END optnewlines
                                | DEFINE ATID COLON full_selector newlines selector_definition END optnewlines
                                | DEFINE ATID COLON uuid LPAREN full_selector RPAREN newlines selector_definition END optnewlines"""

    def p_selector_define_error(self, p):
        """selector_definition : DEFINE error END newlines"""
        self.parser.errok()

    def p_selector_definition(self, p):
        """selector_definition : selector_item newlines selector_definition
                                | empty"""

    def p_selector_pointer(self, p):
        """selector_item : ID EQUALS full_selector
                            | ID COLON full_selector"""

    def p_selector_item_path(self, p):
        """selector_item : ID EQUALS data_path data_type const_value
                            | ID COLON data_path data_type const_value
                            | ID EQUALS data_path data_type
                            | ID COLON data_path data_type"""

    def p_selector_item_vector_path(self, p):
        """selector_item : LESS ID GREATER EQUALS data_path data_type const_value
                            | LESS ID GREATER COLON data_path data_type const_value
                            | LESS ID GREATER EQUALS data_path data_type
                            | LESS ID GREATER COLON data_path data_type"""

    def p_selector_item_tag(self, p):
        """selector_item : CREATE json_object"""

    def p_selector_item_method(self, p):
        """selector_item : function_section"""
    
    def p_selector_item_array(self, p):
        """selector_item : array"""

    def p_selector_item_predicate(self, p):
        """selector_item : predicate"""

    def p_selector_assignment(self, p):
        """selector_assign : ATID EQUALS full_selector optnewlines"""

    ## Array rules
    # Array rule
    def p_array(self, p):
        """array : ARRAY ID LBRACKET const_value TO const_value RBRACKET
                    | ARRAY ID LBRACKET const_value RBRACKET"""

    ## Advancement rules
    # Advancement rule
    def p_advancement(self, p):
        """advancement : ADVANCEMENT ID json_object optnewlines"""

    ## Loot Table rules
    def p_loot_table_type(self, p):
        """loot_table_type : BLOCK
                            | ENTITY"""

    # Loot table rule
    def p_loot_table(self, p):
        """loot_table : LOOT_TABLE loot_table_type ID COLON ID json_object optnewlines
                        | LOOT_TABLE loot_table_type ID json_object optnewlines"""

    ## Predicate rules
    # Predicate rule
    def p_predicate(self, p):
        """predicate : PREDICATE ID json_object optnewlines"""

    ## Item Modifier rules
    # Item Modifier rule
    def p_item_modifier(self, p):
        """item_modifier : ITEM_MODIFIER ID json_object optnewlines"""

    ## Tell / Title rules
    # Tell rule
    def p_tell(self, p):
        """code_block : TELL full_selector string optnewlines"""

    # Title rule
    def p_title(self, p):
        """code_block : TITLE full_selector string optnewlines
                        | SUBTITLE full_selector string optnewlines
                        | ACTIONBAR full_selector string optnewlines"""

    def p_title_times(self, p):
        """code_block : TITLE full_selector const_value const_value const_value string optnewlines
                        | SUBTITLE full_selector const_value const_value const_value string optnewlines
                        | ACTIONBAR full_selector const_value const_value const_value string optnewlines"""

    ## Assignment rules
    # Assignment rule
    def p_assignment(self, p):
        """assign : variable EQUALS expr
                    | variable PLUS_EQUALS expr
                    | variable MINUS_EQUALS expr
                    | variable TIMES_EQUALS expr
                    | variable DIVIDE_EQUALS expr
                    | variable MODULO_EQUALS expr"""
        # TODO: Assignment stuffs

    def p_xcrement(self, p):
        """assign : variable PLUS_PLUS
                    | variable MINUS_MINUS"""
        # TODO: Increment/Decrement stuffs

    def p_return(self, p):
        """assign : RETURN expr"""

    # Constant assignment rule
    def p_constant_assignment(self, p):
        """const_assign : DOLLAR ID EQUALS const_value"""
        # TODO: Constant assignment stuffs

    ## Variable rules
    # Variable rule
    def p_variable_id_variable(self, p):
        """variable : ID DOT ID
                    | full_selector DOT ID"""
        # TODO: Variable assignment

    def p_variable_id(self, p):
        """variable : ID"""
        # TODO: Variable assignment

    def p_variable_constant_integer(self, p):
        """variable : const_int"""

    def p_variable_array(self, p):
        """variable : ID LBRACKET virtual_int RBRACKET
                    | ID LBRACKET expr RBRACKET"""

    def p_variable_array_selector(self, p):
        """variable : full_selector DOT ID LBRACKET virtual_int RBRACKET
                    | full_selector DOT ID LBRACKET expr RBRACKET"""

    def p_variable_path(self, p):
        """variable : LBRACKET ID AT rel_coords RBRACKET DOT ID LBRACKET macro_call_params RBRACKET
                    | LBRACKET ID RBRACKET DOT ID LBRACKET macro_call_params RBRACKET
                    | LBRACKET ID AT rel_coords RBRACKET DOT ID
                    | LBRACKET ID RBRACKET DOT ID"""

    def p_variable_ref(self, p):
        """variable : REF full_selector"""

    def p_variable_storage(self, p):
        """variable : ID COLON data_path
                    | COLON data_path"""

    def p_variable_command(self, p):
        """variable : SUCCESS NEWLINE COMMAND
                    | RESULT NEWLINE COMMAND"""

    def p_variable_virtual_integer(self, p):
        """variable : virtual_int"""

    ## Vector rules
    # Vector rule
    def p_vector_variable(self, p):
        """vector_variable : LESS ID GREATER
                            | full_selector DOT LESS ID GREATER
                            | LESS variable COMMA variable COMMA variable GREATER
                            | const_vector"""

    # Vector expression rule
    def p_vector_expression(self, p):
        """vector_expr : LPAREN vector_expr RPAREN
                        | LESS expr COMMA expr COMMA expr GREATER
                        | full_selector DOT LESS ID GREATER
                        | LESS ID GREATER
                        | HERE LPAREN const_value RPAREN
                        | HERE
                        | const_vector"""
    
    def p_vector_arithmetic(self, p):
        """vector_expr : vector_expr PLUS vector_expr
                        | vector_expr MINUS vector_expr"""

    def p_vector_scalar(self, p):
        """vector_expr : vector_expr PLUS expr
                        | expr PLUS vector_expr
                        | vector_expr MINUS expr
                        | expr TIMES vector_expr
                        | vector_expr TIMES expr
                        | vector_expr DIVIDE expr
                        | vector_expr MODULO expr"""

    def p_vector_negative(self, p):
        """vector_expr : MINUS vector_expr"""

    # Vector assignment rule
    def p_vector_assignment(self, p):
        """assign : vector_variable EQUALS vector_expr
                    | vector_variable PLUS_EQUALS vector_expr
                    | vector_variable MINUS_EQUALS vector_expr"""

    def p_vector_scalar_assignment(self, p):
        """assign : vector_variable EQUALS expr
                    | vector_variable PLUS_EQUALS expr
                    | vector_variable MINUS_EQUALS expr
                    | vector_variable TIMES_EQUALS expr
                    | vector_variable DIVIDE_EQUALS expr
                    | vector_variable MODULO_EQUALS expr"""
        # TODO: Assignment stuffs

    ## Arithmetic rules
    def p_expression_list(self, p):
        """expr_list : expr_list COMMA expr
                        | expr
                        | empty"""

    def p_expression_variable(self, p):
        """expr : variable"""
        p[0] = p[1]

    def p_expression_arithmetic(self, p):
        """expr : expr PLUS expr
                | expr MINUS expr
                | expr TIMES expr
                | expr DIVIDE expr
                | expr MODULO expr"""
        # TODO: Do such arithmetics

    def p_expression_negative(self, p):
        """expr : MINUS expr"""

    def p_expression_power(self, p):
        """expr : expr POWER int"""
        # TODO: Apply such powers

    def p_expression_dot(self, p):
        """expr : vector_expr TIMES vector_expr"""

    def p_expression_function_call(self, p):
        """expr : function_call
                    | method_call"""

    def p_expression_group(self, p):
        """expr : LPAREN expr RPAREN"""

    ## Data rules
    # Data path rule
    def p_data_path(self, p):
        """data_path : ID json_object
                        | ID
                        | FACING"""

    def p_data_path_array(self, p):
        """data_path : ID LBRACKET json_object RBRACKET
                        | ID LBRACKET const_int RBRACKET"""

    def p_data_path_multi(self, p):
        """data_path : data_path DOT data_path"""

    def p_data_type(self, p):
        """data_type : ID"""

        expected = ["byte", "double", "float", "int", "long", "short"]

        if p[1] not in expected:
            self.diagnostics.append(CBDiagnostic(p.slice[1], self.lexer.find_column(self.data, p.slice[1]), self.parser.state, expected))

    ## JSON rules
    # JSON Object rule
    def p_json_object(self, p):
        """json_object : LCURLY optnewlines json_members optnewlines RCURLY"""

    def p_json_object_error(self, p):
        """json_object : LCURLY error RCURLY"""
        self.parser.errok()

    def p_json_members(self, p):
        """json_members : json_pair COMMA optnewlines json_members
                        | json_pair
                        | empty"""

    def p_json_pair(self, p):
        """json_pair : ID COLON optnewlines json_value
                        | string COLON optnewlines json_value
                        | FACING COLON optnewlines json_value
                        | BLOCK COLON optnewlines json_value
                        | PREDICATE COLON optnewlines json_value"""

    def p_json_value(self, p):
        """json_value : DOLLAR ID
                        | JSON
                        | number
                        | string
                        | json_object
                        | json_array
                        | json_literal_array
                        | TRUE
                        | FALSE"""

    def p_json_array(self, p):
        """json_array : LBRACKET optnewlines json_elements optnewlines RBRACKET"""

    def p_json_element(self, p):
        """json_elements : json_value COMMA optnewlines json_elements
                            | json_value
                            | empty"""

    def p_json_literal_array(self, p):
        """json_literal_array : LBRACKET optnewlines ID SEMICOLON optnewlines json_literal_elements optnewlines RBRACKET"""

        expected = ['b', 'i', 'l']

        if p[3].lower() not in expected:
            self.diagnostics.append(CBDiagnostic(p.slice[3], self.lexer.find_column(self.data, p.slice[3]), self.parser.state, expected))

    def p_json_literal_elements(self, p):
        """json_literal_elements : json_literal_value COMMA optnewlines json_literal_elements
                                    | json_literal_value
                                    | empty"""

    def p_json_literal_value(self, p):
        """json_literal_value : DOLLAR ID
                                | number
                                | empty"""
    
    ## NBT rules
    # NBT assignment
    def p_nbt_assignment(self, p):
        """assign : nbt_list EQUALS nbt
                    | nbt_object EQUALS nbt"""

    def p_nbt_append(self, p):
        """assign : nbt_list PLUS_EQUALS nbt"""

    def p_nbt_merge(self, p):
        """assign : nbt_object PLUS_EQUALS nbt"""

    def p_nbt_remove(self, p):
        """code_block : REMOVE nbt_path"""

    def p_nbt_list_entity(self, p):
        """nbt_list : full_selector DOT LBRACKET data_path RBRACKET"""

    def p_nbt_list_storage(self, p):
        """nbt_list : ID COLON LBRACKET data_path RBRACKET
                    | COLON LBRACKET data_path RBRACKET"""

    def p_nbt_object_entity(self, p):
        """nbt_list : full_selector DOT LCURLY data_path RCURLY"""

    def p_nbt_object_storage(self, p):
        """nbt_list : ID COLON LCURLY data_path RCURLY
                    | COLON LCURLY data_path RCURLY"""

    def p_nbt_path_entity(self, p):
        """nbt_path : full_selector DOT data_path"""

    def p_nbt_path_storage(self, p):
        """nbt_object : ID COLON data_path
                    | COLON data_path"""

    def p_nbt_path(self, p):
        """nbt_path : nbt_object
                    | nbt_list"""

    def p_nbt(self, p):
        """nbt : nbt_path
                | json_object
                | string"""

    ## String rules
    # String rule
    def p_string(self, p):
        """string : STRING"""
        p[0] = p[1][1:-1]

    ## Number rules
    # Number rule
    def p_number(self, p):
        """number : int
                    | float"""
        p[0] = p[1]

    # Integer rules
    def p_int(self, p):
        """int : BINARY
                | DECIMAL
                | HEX"""
        if p.slice[1].type == "BINARY":
            p[0] = str(int(p[1], 2))
        elif p.slice[1].type == "HEX":
            p[0] = str(int(p[1], 16))
        else:
            p[0] = p[1]

    # Negative Integer rules
    def p_int_negative(self, p):
        """int : MINUS BINARY
                | MINUS DECIMAL
                | MINUS HEX"""
        if p.slice[2].type == "BINARY":
            p[0] = str(int(p[2], 2))
        elif p.slice[2].type == "HEX":
            p[0] = str(int(p[2], 16))
        else:
            p[0] = str(-int(p[2]))

    # Float rules
    def p_float(self, p):
        """float : FLOAT"""
        p[0] = p[1]

    # Negative Float rules
    def p_float_negative(self, p):
        """float : MINUS FLOAT"""
        p[0] = str(-float(p[2]))

    ## Constant rules
    def p_constant_value(self, p):
        """const_value : const_expr
                        | const_string
                        | const_int"""

    def p_constant_ID(self, p):
        """const_ID : DOLLAR ID"""

    def p_constant_string(self, p):
        """const_string : DOLLAR string"""

    def p_constant_integer(self, p):
        """const_int : int"""

    def p_constant_expression(self, p):
        """const_expr : number
                        | string
                        | const_ID"""

    def p_constant_expression_arithmetic(self, p):
        """const_expr : const_expr PLUS const_expr
                        | const_expr MINUS const_expr
                        | const_expr TIMES const_expr
                        | const_expr DIVIDE const_expr
                        | const_expr MODULO const_expr"""
        # TODO: Do such arithmetics

    def p_constant_expression_compare(self, p):
        """const_expr : const_expr EQUALS_EQUALS const_expr
                        | const_expr LESS const_expr
                        | const_expr LESS_EQUALS const_expr
                        | const_expr GREATER const_expr
                        | const_expr GREATER_EQUALS const_expr"""

    def p_constant_expression_double(self, p):
        """const_expr : const_expr NOT EQUALS const_expr
                        | const_expr TIMES TIMES const_expr"""

    def p_constant_expression_spaced(self, p):
        """const_expr : const_expr OR const_expr
                        | const_expr AND const_expr"""

    def p_constant_expression_negative(self, p):
        """const_expr : MINUS const_expr"""

    def p_constant_expression_list(self, p):
        """const_expr_list : const_expr COMMA optnewlines const_expr_list
                            | const_expr
                            | empty"""

    def p_constant_array(self, p):
        """const_expr : LBRACKET optnewlines const_expr_list optnewlines RBRACKET
                        | LPAREN optnewlines const_expr_list optnewlines RPAREN"""

    def p_constant_array_element(self, p):
        """const_expr : const_expr LBRACKET const_expr RBRACKET"""

    def p_constant_vector(self, p):
        """const_vector : LESS const_expr GREATER"""

    def p_constant_expression_variable(self, p):
        """const_expr : const_expr DOT const_expr"""

    def p_constant_function_call(self, p):
        """const_expr : DOLLAR FUNCTION_ID optnewlines const_expr_list optnewlines RPAREN"""

    ## Virtual Number rules
    # Virtual Number rule
    def p_virtual_number(self, p):
        """virtual_number : number
                            | const_ID"""

    # Virtual Integer rule
    def p_virtual_integer(self, p):
        """virtual_int : int
                        | const_ID"""

    ## MISC rules
    # UUID rule
    def p_uuid(self, p):
        """uuid : int MINUS int MINUS int MINUS int MINUS int"""
    # Newline rule
    def p_newlines(self, p):
        """newlines : newlines NEWLINE
                    | NEWLINE"""
        p[0] = None

    # Optional newline rule
    def p_optnewlines(self, _):
        """optnewlines : newlines
                        | empty"""
        pass

    # Empty rule
    def p_empty(self, _):
        """empty :"""
        pass

    # Error catch-all
    def p_error(self, p):
        if p is None:
            print("Syntax error: unexpected End of File")
        else:
            state = self.parser.state
            expected = [token for token in self.parser.action[state].keys() if not token == "error"]
            self.diagnostics.append(CBDiagnostic(p, self.lexer.find_column(self.data, p), self.parser.state, expected))
            print(self.diagnostics[-1].message)

            # Handle 'dir' not first line
            if self.parser.state == 0: # Initial state, meaning first error we've ran into (Anything but 'dir')
                skip = 0 # Next parsing pass we skip n amount of error tokens
                while True:
                    token = self.parser.token()
                    if not token: # EOF
                        return # TODO: Handle never finding 'dir' token
                    elif token.type == "DIR":
                        break
                    skip += 1

                self.parser.restart() # Don't really think a reset is needed knowing this fires at state 0
                self.parser.errok()

                self.lexer.reset()
                p.lexer.input(p.lexer.lexdata) # Reset lexer tokens
                #p.lexer.lineno = 1 # Reset lexer line number
                for _ in range(skip + 1): # Skip n + 1 to include the first error token we missed
                    token = self.parser.token()
            else:
                pass
                #self.parser.token() # Skip errorneous token

    ### Parser Functions
    def parse(self, data, debug=0):
        #self.lexer.lineno = 1 # Reset lexer every parse
        #self.reset()

        self.data = data
        #return self.parser.parse(data, debug=debug, tracking=True)
        ret =  self.parser.parse(data, debug=debug, tracking=True)
        for i, d in enumerate(self.diagnostics):
            print(f"[{i}]: {d}\n")
        return ret

    def reset(self):
        self.lexer.reset()
        self.parser.errok()
        self.parser.restart()
        self.data = []
        self.diagnostics = []
