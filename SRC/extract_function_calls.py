import ast
import os
from extract_function_defs import extract_function_defs
from get_file_hierarchy import get_file_hierarchy

def extract_function_calls(function_node, user_defined_functions):
    function_calls = []

    class CallVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                if node.func.id in user_defined_functions:
                    function_calls.append(node.func.id)
            self.generic_visit(node)

    visitor = CallVisitor()
    visitor.visit(function_node)

    return function_calls


# Example Usage
# Assuming 'function_node' is an ast.FunctionDef node obtained from AST parsing
# function_calls = extract_function_calls(function_node)
# print(function_calls)


def get_all_user_defined_functions(project_path):
    user_defined_functions = {}
    file_hierarchy = get_file_hierarchy(project_path)

    def process_directory(directory, hierarchy):
        files = hierarchy.get('files', [])
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(project_path, directory, file)
                function_names = extract_function_defs(file_path)
                for func in function_names:
                    user_defined_functions[func] = file_path

        for subdir in hierarchy.get('directories', []):
            new_directory = os.path.join(directory, subdir)
            if subdir in hierarchy:
                process_directory(new_directory, hierarchy[subdir])

    process_directory('', file_hierarchy)
    return user_defined_functions



# # Example Usage
# project_path = r"D:\DKafka Admin\Outsource\Py-Function-Dependency-Extractor\Project_1"
# user_defined_functions = get_all_user_defined_functions(project_path)
# print(user_defined_functions)
