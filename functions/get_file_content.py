import os

from config import MAX_CHARS
from functions.helpers import get_target_path

# file_path parameter is a relative path, but need to make sure it doesn't go
# outside of working directory.
def get_file_content(working_directory: str, file_path: str) -> str:
    target = get_target_path(working_directory, file_path)
    if not target:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target) as fh:
            contents = fh.read(MAX_CHARS)

            if fh.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return contents
    except Exception as e:
        return f"Error: {e}"
