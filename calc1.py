# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, EOF, SPACE, MINUS = 'INTEGER', 'PLUS', 'EOF', 'SPACE', 'MINUS'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self, x):
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if x==1:
            while current_char==' ':
                self.pos+=1
                if self.pos > len(text) - 1:
                    return Token(EOF, None)
                else:
                    current_char = text[self.pos] 

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == ' ':
            token = Token(SPACE, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token(0)
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token(1)

        left = 0
        while self.current_token.type==INTEGER:
            left*=10
            left+=self.current_token.value
            self.current_token = self.get_next_token(0)

        op = self.current_token
        if op.type==SPACE:
            self.current_token = self.get_next_token(1)
        
        while op.type!=EOF:

            if self.current_token.type==PLUS:
                self.current_token = self.get_next_token(1)
                p=1
            elif self.current_token.type==MINUS:
                self.current_token = self.get_next_token(1)
                p=2
            else:
                self.error()

            right = 0
            while self.current_token.type==INTEGER:
                right*=10
                right+=self.current_token.value
                self.current_token = self.get_next_token(0)
            
            op = self.current_token
            if op.type==SPACE:
                self.current_token = self.get_next_token(1)

            if p==1:
                left = left + right
            elif p==2:
                left = left - right
        
        result=left
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()