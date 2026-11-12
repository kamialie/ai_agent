import os

from functions.helpers import get_target_path

def write_file(working_directory: str, file_path: str, content: str) -> str:
    target = get_target_path(working_directory, file_path)
    if not target:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target):
        return f'Error: Cannot write to "{file_path}" as it is a directory' 

    try:
        os.makedirs(os.path.dirname(target),exist_ok=True)
        with open(target, "w") as fh:
            fh.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

