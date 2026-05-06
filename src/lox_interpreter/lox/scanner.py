from lox_interpreter.lox.token import Token
from lox_interpreter.lox.token_type import TokenType, token_mapping


class Scanner:
    """Scanner for the Lox programming language."""

    def __init__(self, source: str):
        self.source: str = source
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.tokens: list[Token] | None = None

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self):
        char = self.advance()
        if char == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif char == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ",":
            self.add_token(TokenType.COMMA)
        elif char == ".":
            self.add_token(TokenType.DOT)
        elif char == "-":
            self.add_token(TokenType.MINUS)
        elif char == "+":
            self.add_token(TokenType.PLUS)
        elif char == ";":
            self.add_token(TokenType.SEMICOLON)
        elif char == "*":
            self.add_token(TokenType.STAR)
        elif char == "!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif char == "=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif char == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif char == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif char == "/":
            if self.match("/"):
                # A comment goes until the end of the line.
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif char in (" ", "\r", "\t"):
            # Ignore whitespace.
            pass
        elif char == '"':
            self.string()
        elif char == "\n":
            self.line += 1
        elif char == "o":
            if self.peek() == "r":
                self.add_token(TokenType.OR)
        else:
            if self.is_digit(char):
                self.number()
            elif self.is_alpha(char):
                self.identifier()
            else:
                print(f"Unexpected character: {char}")

    def identifier(self):
        while self.is_alpha(self.peek()) or self.is_digit(self.peek()):
            self.advance()
        text = self.source[self.start : self.current]
        token_type = token_mapping.get(text, TokenType.IDENTIFIER)
        if token_type is None:
            token_type = TokenType.IDENTIFIER
        self.add_token(token_type)

    def is_alpha(self, char: str) -> bool:
        return (
            (char >= "a" and char <= "z")
            or (char >= "A" and char <= "Z")
            or char == "_"
        )

    def is_alpha_numeric(self, char: str) -> bool:
        return self.is_alpha(char) or self.is_digit(char)

    def is_digit(self, char: str) -> bool:
        return char >= "0" and char <= "9"

    def peek_next(self) -> str:
        """Look at the character after the current one without consuming it."""
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def number(self):
        """Handle number literals."""
        while self.peek().isdigit():
            self.advance()
        # Look for a fractional part.
        if self.peek() == "." and self.peek_next().isdigit():
            # Consume the "."
            self.advance()
            while self.peek().isdigit():
                self.advance()
        value = float(self.source[self.start : self.current])
        self.add_token(TokenType.NUMBER, value)

    def string(self):
        """Handle string literals."""
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            print("Unterminated string.")
            return
        # The closing ".
        self.advance()
        # Trim the surrounding quotes.
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def peek(self) -> str:
        """Look at the current character without consuming it."""
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def advance(self) -> str:
        """Consume the current character and return it."""
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal: object | None = None):
        text = self.source[self.start : self.current]
        if self.tokens is None:
            self.tokens = []
        self.tokens.append(Token(token_type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        """Methods that check if the next character is the expected one.
        It is like a conditional advance where we consume the character only if the character found is the
        one expected. If the source is already finished we return False without consuming anything.

        Args:
            expected (str): Expected character.

        Returns:
            bool: True if the character matched, False otherwise.
        """
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
