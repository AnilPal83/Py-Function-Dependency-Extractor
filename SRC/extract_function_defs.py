import ast

def extract_function_defs(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Parse the file content into an AST
    tree = ast.parse(file_content)

    # Function to extract function names
    def extract_funcs(node):
        functions = []
        for elem in node.body:
            if isinstance(elem, ast.FunctionDef):
                functions.append(elem.name)
        return functions

    return extract_funcs(tree)



# # Example Usage
# file_path = r"D:\DKafka Admin\Outsource\Py-Function-Dependency-Extractor\Project_1\simulate.py"
# function_names = extract_function_defs(file_path)
# print(function_names)
