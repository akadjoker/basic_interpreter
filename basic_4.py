

TK_INT = 'INT'
TK_FLOAT = 'FLOAT'

TK_IDENTIFIER = 'IDENTIFIER'
TK_KEYWORD ='KEYWORD'

TK_PLUS  = 'PLUS'
TK_MINUS = 'MINUS'
TK_MUL = 'MUL'
TK_DIV = 'DIV'
TK_POW = 'POW' # ^
TK_MOD = 'MOD' # %
TK_EQ  =  'EQ' # =

TK_COMMA = 'COMMA' # ,     
TK_SEMICOLON = 'SEMICOLON' #;

TK_VAR =  'VAR'
TK_EXIT = 'EXIT'

TK_LPAREN = 'LPAREN'
TK_RPAREN = 'RPAREN'
TK_LBRACE = 'LBRACE'
TK_RBRACE = 'RBRACE'

TK_ERROR = 'ERROR'


KEYWORDS = [
    'var',
    'exit',
    'div',
    'mod',
    'and',
    'or',
    'not',
    'xor',
]

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def match(self, type, value):
        return self.type == type and self.value == value

    def __str__(self):
        return f'{self.type}:{self.value}'

    def __repr__(self):
        return self.__str__()

    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.column = 0
        self.line = 1
        self.current_char = self.text[self.pos]
        self.size = len(self.text)
    
    def error(self,msg):
        print("Invalid character '{}' found at line: {}, column: {}".format(msg,self.line, self.column))
        exit(1)

    
    def advance(self):
        self.pos += 1
        self.column += 1
        if self.pos < self.size:
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            token = Token(TK_FLOAT, float(result), self.line, self.column)
        else:
            token = Token(TK_INT, int(result), self.line, self.column)
        return token

    def identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum() or self.current_char == '_':
            result += self.current_char
            self.advance()
        id_str = result.lower()
        if id_str in KEYWORDS:
            token = Token(TK_KEYWORD, id_str, self.line, self.column)
        else:
            token = Token(TK_IDENTIFIER, id_str, self.line, self.column)
        return token

    def get_next_token(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                if self.current_char == '\n':
                    self.line += 1
                    self.column = 0
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                token=  self.integer()
                tokens.append(token)
            
            elif self.current_char.isalpha() or self.current_char == '_':
                token = self.identifier()
                tokens.append(token)
            
            
            elif self.current_char == '+':
                token = Token(TK_PLUS, '+', self.line, self.column)
                self.advance()
                tokens.append(token)
           
            elif self.current_char == '^':
                token = Token(TK_POW, '^', self.line, self.column)
                self.advance()
                tokens.append(token)
             
            elif self.current_char == '%':
                token = Token(TK_MOD, '%', self.line, self.column)
                self.advance()
                tokens.append(token)

            elif self.current_char == '-':
                token = Token(TK_MINUS, '-', self.line, self.column)
                self.advance()
                tokens.append(token)
           
            
            elif self.current_char == '*':
                token = Token(TK_MUL, '*', self.line, self.column)
                self.advance()
                tokens.append(token)
             
            
            elif self.current_char == '/':
                token = Token(TK_DIV, '/', self.line, self.column)
                self.advance()
                tokens.append(token)
            elif self.current_char == '=':
                token = Token(TK_EQ, '=', self.line, self.column)
                self.advance()
                tokens.append(token)
            elif self.current_char == ',':
                token = Token(TK_COMMA, ',', self.line, self.column)
                self.advance()
                tokens.append(token)
            elif self.current_char == ';':
                token = Token(TK_SEMICOLON, ';', self.line, self.column)
                self.advance()
                tokens.append(token)
            elif self.current_char == '{':
                token = Token(TK_LBRACE, '{', self.line, self.column)
                self.advance()
                tokens.append(token)
            elif self.current_char == '}':
                token = Token(TK_RBRACE, '}', self.line, self.column)
                self.advance()
                tokens.append(token)
            elif self.current_char == '(':
                token = Token(TK_LPAREN, '(', self.line, self.column)
                self.advance()
                tokens.append(token)
            elif self.current_char == ')':
                token = Token(TK_RPAREN, ')', self.line, self.column)
                self.advance()
                tokens.append(token)
            else:  
                self.error(self.current_char)
        
        token = Token('EOF', None, self.line, self.column)
        tokens.append(token)
        return tokens


class NumberNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.column = token.column
        self.line = token.line
    
    def __repr__(self):
        return f'{self.token}'
    
class VarAccessNode:
    def __init__(self, var_name):
        self.var_name = var_name
        self.column = var_name.column
        self.line = var_name.line
    
    def __repr__(self):
        return f'{self.var_name}'
    
class VarAssignNode:
    def __init__(self, var_name, value_node):
        self.var_name = var_name
        self.value = value_node
        self.column = var_name.column
        self.line = var_name.line
    
    def __repr__(self):
        return f'({self.var_name}, {self.value})'
    
class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        self.column = right.column
        self.line = left.line
    
    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'


class UnaryOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node
        self.column = node.column
        self.line = node.line
    
    def __repr__(self):
        return f'({self.op}, {self.node})'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.size = len(self.tokens)
        self.current_token = self.tokens[self.pos]

    def error(self,msg):
        print('Invalid syntax ',msg)
        exit(1)

    def advance(self):
        self.pos += 1
        if self.pos < self.size:
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def atom(self):
        token = self.current_token
        if token.type == TK_INT:
            self.advance()
            return NumberNode(token)
        elif token.type == TK_FLOAT:
            self.advance()
            return NumberNode(token)
        elif token.type == TK_IDENTIFIER:
            self.advance()
            return VarAccessNode(token)
        elif token.type == TK_LPAREN:
            self.advance()
            node = self.expr()
            if self.current_token.type != TK_RPAREN:
                self.error("(factor) Expected ')' at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
            self.advance()
            return node
    
        self.error(f"(atom) Expected: \n  var, int, float, '(', or operator at Line: {token.line} Col :{token.column+1}")
    

    def power(self):
        node = self.atom()
        while self.current_token is not None and self.current_token.type == TK_POW:
            token = self.current_token
            if token.type == TK_POW:
                self.advance()
            node = BinOpNode(node, token, self.factor())
        return node

    def factor(self):
        token = self.current_token

        if token.type in ( TK_PLUS, TK_MINUS):
            self.advance()
            node = UnaryOpNode(token, self.factor())
            return node
        return self.power()
        
    def term(self):
        node = self.factor()
        while self.current_token is not None and self.current_token.type in (TK_MUL, TK_DIV):
            token = self.current_token
            if token.type == TK_MUL:
                self.advance()
            elif token.type == TK_DIV:
                self.advance()
            node = BinOpNode(node, token, self.factor())
        return node
    
    def expr(self):

        if self.current_token.match(TK_KEYWORD,'exit'):
            self.advance()
            if self.current_token.match(TK_LPAREN,'('):
                self.advance()
                if self.current_token.match(TK_RPAREN,')'):
                    self.advance()
                else:
                    self.error("Expected ')' at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
            else:
                self.error("Expected '(' at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
        
        #aqui podmeos voltar a atribuição de variaveis    
        # if self.current_token.type == TK_IDENTIFIER:
        #     var_name = self.current_token
        #     self.advance()
        #     if self.current_token.type != TK_EQ:
        #         self.error("Expected '=' at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
        #     self.advance()
        #     node = self.expr()
        #     return VarAssignNode(var_name, node)

        if self.current_token.match(TK_KEYWORD,'var'):
            self.advance()
            if self.current_token.type != TK_IDENTIFIER:
                self.error("Expected Identifier at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))

            var_name = self.current_token
            self.advance()
            if self.current_token.type != TK_EQ:
                self.error("Expected '=' at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
            
            self.advance()
            node = self.expr()


            return VarAssignNode(var_name, node)
        


        node = self.term()
        if node==None and self.current_token is not None:
            self.error("(expr) Expected var, int, float,'+', '-' or '%' at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))



        while self.current_token is not None and self.current_token.type in (TK_PLUS, TK_MINUS, TK_MOD):
            token = self.current_token
            if token.type == TK_PLUS:
                self.advance()
            elif token.type == TK_MINUS:
                self.advance()
            elif token.type == TK_MOD:
                self.advance()

            else:
                self.error("(expr) Expected '+', '-' or '%' at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
            node = BinOpNode(node, token, self.term())
        
        return node
    
    def parse(self):
        res= self.expr()
        if self.current_token.type != 'EOF':
            print(self.current_token)
            self.error("(parse)  at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
        return res
    
    def bin_op(self, fun_a, ops, func_b=None):
        if  func_b ==None:
            func_b = fun_a
        left = fun_a()
        while self.current_token.type  in ops:
            token = self.current_token
            self.advance()
            right = func_b()
            left = BinOpNode(left, token, right)
        return left    


class Number:
    def __init__(self, value, line=None, column=None):
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f'{self.value}'
    
    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
    
    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
    
    def mul(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
    
    def mulby(self, other):
        return Number(self.value * other)
    
    def div(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                print(f"Division by zero At Line: {other.line} : Column: {other.column} "  )
                exit(1)
            return Number(self.value / other.value)
    def powed(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value)
        
    def mod(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value)
        
    def __repr__(self):
        return f'{self.value}'



class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
    
    def __repr__(self):
        return f'{self.vars}'
    
    def get(self, var_name):
        if var_name in self.vars:
            return self.vars[var_name]
        elif self.parent:
            return self.parent.get(var_name)
        else:
            print(f"Undefined variable '{var_name}'")
            exit(1)
    
    def set(self, var_name, value):
        self.vars[var_name] = value

    def remove(self, var_name):
        del self.vars[var_name]


class Interpreter:
    def __init__(self, parser, context):
        self.parser = parser
        self.context = context
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)
    
    def visit_VarAssignNode(self, node):
        var_name = node.var_name.value
        value = self.visit(node.value)

        if value == None:
            print(f"Undefined variable '{var_name}'")
            exit(1)

        self.context.symbol_table.set(var_name, value)

  

        return value
    
    def visit_VarAccessNode(self, node):
        var_name = node.var_name.value
        value = self.context.symbol_table.get(var_name)

        if value == None:
            print(f"Undefined variable '{var_name}'")
            exit(1)
        return value

    def visit_NumberNode(self, node):
        #print("visit_NumberNode")
        return Number(node.value, node.line, node.column)
    
    def visit_BinOpNode(self, node):
        #print("visit_BinOpNode")
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == TK_PLUS:
            return left.add(right)
        elif node.op.type == TK_MINUS:
            return left.sub(right)
        elif node.op.type == TK_MUL:
            return left.mul(right)
        elif node.op.type == TK_DIV:
            return left.div(right)
        elif node.op.type == TK_POW:
            return left.powed(right)
        elif node.op.type == TK_MOD:
            return left.mod(right)
    
    def visit_UnaryOpNode(self, node):
        #print("visit_UnaryOpNode")
        number = self.visit(node.node)
       
        if node.op.type == TK_MINUS:
            number = number.mul(Number(-1, node.line, node.column)) 
        return number 

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)



global_symbol_table = Environment()
global_symbol_table.set("nil", Number(0))
global_symbol_table.set("true", Number(1))
global_symbol_table.set("false", Number(0))


while True:
    try:
        text = input('basic> ')
    except EOFError:
        break
    if not text:
        continue
    
    lexer = Lexer(text)
    tokens = lexer.get_next_token()
    parser = Parser(tokens)
    
    context = Context('<program>')
    context.symbol_table = global_symbol_table


    interpreter = Interpreter(parser, context)
    re = interpreter.interpret()
    print(re)
