class Runner:
    def __init__(self):
        had_error = False

    def run_file(self, path: str):
        with open(path, "r", encoding="UTF-8") as file:
            source = file.read()
        self.run(source)

    def run(self, source: str):
        print(source)

    def run_repl(self):
        """Run LOX in REPL mode"""
        while True:
            try:
                line = input("> ")
                self.run(line)
            except EOFError:
                break
