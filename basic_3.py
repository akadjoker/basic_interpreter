

TK_INT = 'INT'
TK_FLOAT = 'FLOAT'
TK_PLUS = 'PLUS'
TK_MINUS = 'MINUS'
TK_MUL = 'MUL'
TK_DIV = 'DIV'
TK_LPAREN = 'LPAREN'
TK_RPAREN = 'RPAREN'
TK_ERROR = 'ERROR'

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

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
            
            
            elif self.current_char == '+':
                token = Token(TK_PLUS, '+', self.line, self.column)
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

    def factor(self):
        token = self.current_token

        if token.type in ( TK_PLUS, TK_MINUS):
            self.advance()
            node = UnaryOpNode(token, self.factor())
            return node
        if token.type == TK_INT:
            self.advance()
            return NumberNode(token)
        elif token.type == TK_FLOAT:
            self.advance()
            return NumberNode(token)
        elif token.type == TK_LPAREN:
            self.advance()
            node = self.expr()
            if self.current_token.type != TK_RPAREN:
                self.error("(factor) Expected ')' at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
            self.advance()
            return node
        self.error(f"(factor) Expected int or float at Line: {token.line} Col :{token.column+1}")
        
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
        node = self.term()
        while self.current_token is not None and self.current_token.type in (TK_PLUS, TK_MINUS):
            token = self.current_token
            if token.type == TK_PLUS:
                self.advance()
            elif token.type == TK_MINUS:
                self.advance()
            else:
                self.error("(expr) Expected +, - at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
            node = BinOpNode(node, token, self.term())
        return node
    
    def parse(self):
        res= self.expr()
        if self.current_token.type != 'EOF':
            self.error("(parse) Expected +, -, * or / at Line: {}, Col: {}".format(self.current_token.line, self.current_token.column+1))
        return res
    
    def bin_op(self, fun, ops):
        node = fun()
        while self.current_token is not None and self.current_token.type in ops:
            token = self.current_token
            if token.type == TK_PLUS:
                self.advance()
            elif token.type == TK_MINUS:
                self.advance()
            node = BinOpNode(node, token, fun())
        return node
    


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
        
    def __repr__(self):
        return f'{self.value}'

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)
    
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
    
    def visit_UnaryOpNode(self, node):
        #print("visit_UnaryOpNode")
        number = self.visit(node.node)
       
        if node.op.type == TK_MINUS:
            number = number.mul(Number(-1, node.line, node.column)) 
        return number 

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

while True:
    try:
        text = input('calc> ')
    except EOFError:
        break
    if not text:
        continue
    
    lexer = Lexer(text)
    tokens = lexer.get_next_token()
    parser = Parser(tokens)
  
    interpreter = Interpreter(parser)
    re = interpreter.interpret()
    print(re)