import ast

def get_function_source_code(file_path, function_name):
    with open(file_path, 'r') as file:
        file_content = file.read()

    tree = ast.parse(file_content)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return ast.get_source_segment(file_content, node)
    return None
