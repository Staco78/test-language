from error import *
import _types as types
from memory import *
import string

DIGITS = "0123456789"
LETTERS = string.ascii_letters
WORD_CONTENT = LETTERS + DIGITS + "_"


TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIVIDE = "DIVIDE"
TT_FLOAT = "FLOAT"
TT_INT = "INT"
TT_LPARENT = "("
TT_RPARENT = ")"
TT_KEYWORD = "KEYWORD"
TT_IDENTIFIER = "IDENTIFIER"
TT_EQ = "EQ"
TT_EE = "EE"
TT_NE = "NE"
TT_GT = "GT"
TT_GTE = "GTE"
TT_LT = "LT"
TT_LTE = "LTE"
TT_AND = "AND"
TT_NOT = "NOT"
TT_OR = "OR"


KEYWORDS = [
    "let"
]


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}" if self.value != None else f"{self.type}"


class Lexer:
    def __init__(self, text, ln):
        self.pos = -1
        self.text = text
        self.ln = ln
        self.advance()

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char == " ":
                self.advance()
            elif self.current_char in DIGITS + ".":
                tokens.append(self.detect_number())
            elif self.current_char in LETTERS:
                tokens.append(self.detect_word())
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIVIDE))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPARENT))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPARENT))
                self.advance()
            elif self.current_char == "=":
                tokens.append(self.detect_equal())
            elif self.current_char == "!":
                tokens.append(self.detect_not_equals())
            elif self.current_char == "<":
                tokens.append(self.detect_less())
            elif self.current_char == ">":
                tokens.append(self.detect_greater())
            elif self.current_char == "&":
                token, error = self.detect_and()
                if error:
                    return None, error
                tokens.append(token)
            elif self.current_char == "|":
                token, error = self.detect_or()
                if error:
                    return None, error
                tokens.append(token)
            else:
                return None, IllegalCharError(f'"{self.current_char}"')
        return tokens, None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(
            self.text) else None

    def detect_number(self):
        number = ""
        dot_count = 0
        type_ = TT_INT
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == ".":
                type_ = TT_FLOAT
                dot_count += 1
                if dot_count == 2:
                    break
            number += self.current_char
            self.advance()
        if number.startswith("."):
            number = "0" + number
        return Token(type_, number)

    def detect_word(self):
        word = self.current_char
        self.advance()

        while self.current_char != None and self.current_char in WORD_CONTENT:
            word += self.current_char
            self.advance()

        if word in KEYWORDS:
            return Token(TT_KEYWORD, word)
        return Token(TT_IDENTIFIER, word)

    def detect_equal(self):
        self.advance()
        if self.current_char == "=":
            self.advance()
            return Token(TT_EE)
        return Token(TT_EQ)

    def detect_not_equals(self):
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TT_NE)
        return Token(TT_NOT)

    def detect_less(self):
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TT_LTE)
        return Token(TT_LT)

    def detect_greater(self):
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TT_GTE)
        return Token(TT_GT)

    def detect_and(self):
        self.advance()

        if self.current_char == "&":
            self.advance()
            return Token(TT_AND), None
        return None, UnexpectedCharError(f"'&' expected after '&' not '{self.current_char}'")

    def detect_or(self):
        self.advance()

        if self.current_char == "|":
            self.advance()
            return Token(TT_OR), None
        return None, UnexpectedCharError(f"'|' expected after '|' not '{self.current_char}'")


class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class DefineVarNode:
    def __init__(self, var_name_token, node, create=True):
        self.var_name_token = var_name_token
        self.node = node
        self.create = create

    def __repr__(self):
        return f"define {self.var_name_token} at {self.node}"


class AccessVarNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

    def __repr__(self):
        return f"access {self.var_name_token}"

class InverseNode:
    def __init__(self, node):
        self.node = node

    def __repr__(self):
        return f"!{self.node}"

######### PARSER ##########


class ParserRegister:
    def __init__(self):
        self.error = None
        self.result = None

    def register(self, res):
        if isinstance(res, ParserRegister):
            self.error = res.error
            self.result = res.result
            return res.result
        self.result = res
        return res

    def failed(self, error):
        self.error = error
        return self


# class t:
#     def __init__(self, tokens):
#         self.tokens = tokens
#         self.pos = -1
#         self.register = ParserRegister()
#         self.advance()

#     def advance(self):
#         self.pos += 1
#         if self.pos < len(self.tokens):
#             self.current_tok = self.tokens[self.pos]
#         return self.current_tok

#     def parse(self):
#         self.expr()
#         return self.register

#     def factor(self):
#         tok = self.current_tok

#         if tok.type in (TT_PLUS, TT_MINUS):
#             self.advance()
#             factor = self.factor()
#             return UnaryOpNode(tok, factor)

#         elif tok.type in (TT_INT, TT_FLOAT):
#             self.advance()
#             return self.register.register(NumberNode(tok))

#         elif tok.type == TT_LPARENT:
#             self.advance()
#             expr = self.expr()
#             if self.current_tok.type == TT_RPARENT:
#                 self.advance()
#                 return self.register.register(expr)
#             else:
#                 return self.register.failed(InvalidSyntaxError("Expected ')'"))

#         elif tok.type == TT_KEYWORD:
#             return self.register.register(self.keyword(tok))

#         elif tok.type == TT_IDENTIFIER:
#             self.advance()
#             if self.current_tok.type == TT_EQ:
#                 self.advance()
#                 return self.register.register(DefineVarNode(tok, self.register.register(self.expr()), False))
#             return self.register.register(AccessVarNode(tok))

#         return self.register.failed(InvalidSyntaxError("Expected int or float"))

#     def term(self):
#         return self.bin_op(self.factor, (TT_MUL, TT_DIVIDE))

#     def expr(self):
#         return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

#     def keyword(self, token):
#         if token.value == "let":
#             self.advance()
#             if self.current_tok.type == TT_IDENTIFIER:
#                 var_name = self.current_tok
#                 self.advance()
#                 if self.current_tok.type == TT_EQ:
#                     self.advance()
#                     return self.register.register(DefineVarNode(var_name, self.register.register(self.expr())))
#                 else:
#                     return self.register.register(DefineVarNode(var_name, undefined()))
#             else:
#                 return self.register.failed(RuntimeError("Expected identifier"))

#     def bin_op(self, func, ops):
#         left = func()
#         while self.current_tok.type in ops:
#             op_tok = self.current_tok
#             self.advance()
#             right = func()
#             left = BinOpNode(left, op_tok, right)
#         return self.register.register(left)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.advance()

    def parse(self):
        return self.expr()


    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_tok = self.tokens[self.pos]
        return self.current_tok

    def bin_op(self, ops, func):
        left = func()

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)

        return left


    def expr(self):
        if self.current_tok.type == TT_KEYWORD:
            if self.current_tok.value == "let":
                self.advance()
                if self.current_tok.type == TT_IDENTIFIER:
                    var_name = self.current_tok
                    self.advance()
                    if self.current_tok.type == TT_EQ:
                        self.advance()
                        return DefineVarNode(var_name, self.expr())
                    else:
                        return DefineVarNode(var_name, undefined())
                else:
                    raise RuntimeError("Expected identifier")
                
        return self.bin_op((TT_AND, TT_OR), self.comp_expr)

    def comp_expr(self):
        if self.current_tok == TT_NOT:
            self.advance()
            return InverseNode(self.expr())

        return self.bin_op((TT_EE, TT_NE, TT_GT, TT_GTE, TT_LT, TT_LTE), self.arith_expr)

    def arith_expr(self):
        return self.bin_op((TT_PLUS, TT_MINUS), self.term)

    def term(self):
        return self.bin_op((TT_MUL, TT_DIVIDE), self.factor)

    def factor(self):
        token = self.current_tok
        if self.current_tok.type in (TT_PLUS, TT_MINUS):
            self.advance()
            return UnaryOpNode(token, self.factor())

        return self.atom()

    def atom(self):
        token = self.current_tok

        if self.current_tok.type == TT_INT or self.current_tok.type == TT_FLOAT:
            self.advance()
            return NumberNode(token)
        elif self.current_tok.type == TT_IDENTIFIER:
            self.advance()
            return AccessVarNode(token)
        elif self.current_tok.type == TT_LPARENT:
            self.advance()
            expr = self.expr()
            if self.current_tok == TT_RPARENT:
                self.advance()
                return expr
            raise InvalidSyntaxError("Expected ')'")

    

        


##################################
#########   RUNTIME     ##########
##################################

class RuntimeRegister:
    def __init__(self):
        self.error = None
        self.result = None

    def register(self, res):
        if isinstance(res, RuntimeRegister):
            self.error = res.error
            self.result = res.result
            return res.result
        self.result = res
        return res

    def failed(self, error):
        self.error = error
        return self


class Runtime:
    def exec(self, node):
        method_name = f'exec_{type(node).__name__}'
        method = getattr(self, method_name, self.no_exec_method)
        register = RuntimeRegister()
        register.register(method(node))
        return register

    def no_exec_method(self, node):
        raise Exception(f'No exec_{type(node).__name__} method defined')

    def exec_NumberNode(self, node):
        register = RuntimeRegister()
        return register.register(types.Number(node.tok.value))

    def exec_BinOpNode(self, node):
        register = RuntimeRegister()
        left = register.register(self.exec(node.left_node))
        if register.error:
            return register
        right = register.register(self.exec(node.right_node))
        if register.error:
            return register

        if node.op_tok.type == TT_PLUS:
            result, error = left.add(right)
            if error:
                return register.failed(error)
            return register.register(result)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.min(right)
            if error:
                return register.failed(error)
            return register.register(result)
        elif node.op_tok.type == TT_MUL:
            result, error = left.mul(right)
            if error:
                return register.failed(error)
            return register.register(result)
        elif node.op_tok.type == TT_DIVIDE:
            result, error = left.divide(right)
            if error:
                return register.failed(error)
            return register.register(result)

    def exec_UnaryOpNode(self, node):
        register = RuntimeRegister()
        number = register.register(self.exec(node.node))

        if node.op_tok.type == TT_MINUS:
            number = register.register(types.Number(-number.value))

        return register

    def exec_DefineVarNode(self, node):
        register = RuntimeRegister()
        if not node.create:
            if not global_object.exist(node.var_name_token.value):
                return register.failed(RuntimeError(f"{node.var_name_token.value} does not exist"))
        global_object.set(node.var_name_token.value, register.register(
            self.exec(node.node)) if not isinstance(node.node, undefined) else undefined)
        return register

    def exec_AccessVarNode(self, node):
        register = RuntimeRegister()
        register.register(global_object.get(node.var_name_token.value))
        return register


global_object = symbolTable()
global_object.set("undefined", types.undefined())
global_object.set("true", types.Boolean(types.true))
global_object.set("false", types.Boolean(types.false))


# RUN #

def run(text):
    tokens, error = Lexer(text, 0).make_tokens()
    if error:
        return None, error
    if tokens == []:
        return "", None
    print(tokens)

    parser = Parser(tokens)
    result = parser.parse()
    print(result)

    runtime = Runtime()
    runtime_result = runtime.exec(result)
    if runtime_result.error:
        return None, runtime_result.error

    return runtime_result.result, None
