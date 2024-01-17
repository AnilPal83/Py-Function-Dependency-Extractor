import os

def get_file_hierarchy(root_dir):
    file_hierarchy = {}

    for root, dirs, files in os.walk(root_dir):

        # Get relative path from the root_dir
        rel_path = os.path.relpath(root, root_dir)

        if rel_path == '.':
            rel_path = ''

        # Initialize dictionary for this path if not already present
        current_level = file_hierarchy
        if rel_path != '':
            for part in rel_path.split(os.sep):
                current_level = current_level.setdefault(part, {})

        # Add files and directories to the current level
        current_level['files'] = files
        current_level['directories'] = dirs


    return file_hierarchy

# # Example Usage
# project_path = r"D:\DKafka Admin\Outsource\Py-Function-Dependency-Extractor\Project_1"
# hierarchy = get_file_hierarchy(project_path)
# print("\nFinal Hierarchy of files:")
# print(hierarchy)
