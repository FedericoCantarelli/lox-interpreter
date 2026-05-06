from lox_interpreter.lox.token import Token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0


# class Parser {
# private final List<Token> tokens;
# private int current = 0;
# Parser(List<Token> tokens) {
# this.tokens = tokens;
# }
