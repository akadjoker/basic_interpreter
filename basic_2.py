

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
    
    def __repr__(self):
        return f'{self.token}'
    
class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'


class UnaryOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node
    
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
    tree = parser.parse()
    print(tree)
    