import click


@click.group()
def ast():
    pass


@ast.command()
@click.argument("output_dir", type=click.Path(exists=True))
def generate(output_dir):
    define_ast(
        output_dir,
        "expr",
        [
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : Object Value",
            "Unary    : Token operator, Expr right",
        ],
    )


def define_ast(output_dir: str, base_name: str, types: list[str]):
    path = output_dir + "/" + base_name.lower() + ".py"

    with open(path, "w", encoding="utf-8") as writer:

        def w(line=""):
            writer.write(line + "\n")

        w("from __future__ import annotations")
        w("from abc import ABC, abstractmethod")
        w("from typing import Any, Generic, TypeVar")
        w()
        w("R = TypeVar('R')")
        w()

        # Visitor interface
        define_visitor(w, base_name, types)

        # Base class
        w(f"class {base_name}(ABC):")
        w("    @abstractmethod")
        w(f"    def accept(self, visitor: '{base_name}Visitor[R]') -> R:")
        w("        ...")
        w()

        # Subclasses
        for type_def in types:
            class_name = type_def.split(":")[0].strip()
            fields = type_def.split(":")[1].strip()
            define_type(w, base_name, class_name, fields)


def define_visitor(w, base_name: str, types: list[str]):
    w(f"class {base_name}Visitor(ABC, Generic[R]):")
    for type_def in types:
        type_name = type_def.split(":")[0].strip()
        w("    @abstractmethod")
        w(
            f"    def visit_{type_name.lower()}_{base_name.lower()}(self, {base_name.lower()}: '{type_name}') -> R:"
        )
        w("        ...")
        w()
    w()


def define_type(w, base_name: str, class_name: str, field_list: str):
    fields = [f.strip() for f in field_list.split(",")]

    w(f"class {class_name}({base_name}):")

    # __init__
    typed_params = ", ".join(
        f"{f.lower().split()[-1]}: Any" for f in fields
    )  # name: Any
    w(f"    def __init__(self, {typed_params}):")
    for field in fields:
        name = field.split()[-1]
        w(f"        self.{name.lower()} = {name.lower()}")
    w()

    # accept()
    w(f"    def accept(self, visitor: '{base_name}Visitor[R]') -> R:")
    w(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)")
    w()
