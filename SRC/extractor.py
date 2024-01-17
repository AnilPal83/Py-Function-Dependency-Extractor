import ast
import json
import os
from build_dependency_graph import build_dependency_graph
from extract_function_calls import get_all_user_defined_functions
from get_function_source_code import get_function_source_code

class FunctionNode:
    def __init__(self, name, source_code):
        self.name = name
        self.source_code = source_code
        self.children = []

    def to_dict(self):
        return {
            "name": self.name,
            "source_code": self.source_code,
            "functions_called": [child.to_dict() for child in self.children]
        }


def build_function_tree(dependency_graph, function_defs):
    nodes = {name: FunctionNode(name, function_defs[name]["source_code"]) for name in dependency_graph}

    for function, calls in dependency_graph.items():
        node = nodes[function]
        for called_function in calls:
            if called_function in nodes:
                node.children.append(nodes[called_function])

    return nodes


def Py_Function_Dependency_Extractor(project_filepath):
    dependency_graph = build_dependency_graph(project_filepath)
    user_defined_functions_info = get_all_user_defined_functions(project_filepath)

    function_defs = {}
    for func_name, file_path in user_defined_functions_info.items():
        source_code = get_function_source_code(file_path, func_name)
        function_defs[func_name] = {
            "name": func_name,
            "source_code": source_code
        }

    return build_function_tree(dependency_graph, function_defs)


# project_path = r"D:\DKafka Admin\Outsource\Py-Function-Dependency-Extractor\Project_1"
# function_tree = Py_Function_Dependency_Extractor(project_path)

# function_tree_json = {name: node.to_dict() for name, node in function_tree.items()}
# print("\nFunction Tree (JSON):")
# print(json.dumps(function_tree_json, indent=4))

