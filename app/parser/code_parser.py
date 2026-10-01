from tree_sitter import Language, Parser
import tree_sitter_python


PYTHON_LANGUAGE = Language(tree_sitter_python.language())
parser = Parser(PYTHON_LANGUAGE)


def parse_python_code(code: str):
    tree = parser.parse(code.encode("utf-8"))

    return tree.root_node


def extract_code_structure(code: str):
    tree = parse_python_code(code)

    functions = []
    classes = []

    def walk(node):
        if node.type == "function_definition":
            name_node = node.child_by_field_name("name")

            if name_node:
                functions.append(name_node.text.decode("utf-8"))

        elif node.type == "class_definition":
            name_node = node.child_by_field_name("name")

            if name_node:
                classes.append(name_node.text.decode("utf-8"))

        for child in node.children:
            walk(child)

    walk(tree)

    return {
        "functions": functions,
        "classes": classes,
    }
