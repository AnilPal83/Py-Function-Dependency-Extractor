
from typing import Optional
import json

from flask import Flask, request, jsonify

# Import your existing functions
from extractor import Py_Function_Dependency_Extractor

app = Flask(__name__)

@app.route('/function_dependency_tree', methods=['POST'])
def function_dependency_tree():
    data = request.json
    project_path = data.get("project_path")
    
    if not project_path:
        return jsonify({"error": "No project path provided"}), 400

    try:
        function_tree = Py_Function_Dependency_Extractor(project_path)
        # Convert the tree to a dictionary format
        function_tree_json = {name: node.to_dict() for name, node in function_tree.items()}
        return jsonify(function_tree_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

