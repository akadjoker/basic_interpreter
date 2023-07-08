

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
        return f'{self.type}, {self.value}'

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
        #tokens.append(token)
        return tokens


while True:
    try:
        text = input('calc> ')
    except EOFError:
        break
    if not text:
        continue
    
    lexer = Lexer(text)
    tokens = lexer.get_next_token()
    print(tokens)