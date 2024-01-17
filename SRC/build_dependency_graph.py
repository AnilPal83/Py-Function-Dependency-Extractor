import os
import ast
from extract_function_defs import extract_function_defs
from extract_function_calls import extract_function_calls, get_all_user_defined_functions

# Helper function to get full path of all python files in the directory tree
def get_all_python_files(path):
    python_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def build_dependency_graph(project_path):
    dependency_graph = {}
    user_defined_functions_info = get_all_user_defined_functions(project_path)
    user_defined_functions = set(user_defined_functions_info.keys())

    python_files = get_all_python_files(project_path)

    for file_path in python_files:
        function_defs = extract_function_defs(file_path)

        with open(file_path, 'r') as file:
            file_content = file.read()
        tree = ast.parse(file_content)

        for func in function_defs:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func:
                    calls = extract_function_calls(node, user_defined_functions)

                    if func not in dependency_graph:
                        dependency_graph[func] = []
                    dependency_graph[func].extend(calls)

    return dependency_graph
