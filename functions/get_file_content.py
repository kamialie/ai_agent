import os

from config import MAX_CHARS

# file_path parameter is a relative path, but need to make sure it doesn't go
# outside of working directory.
def get_file_content(working_directory: str, file_path: str) -> str:
    abs_workdir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_workdir, file_path))
    try:
        if not os.path.commonpath([abs_workdir, abs_file_path]) == abs_workdir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path) as fh:
            contents = fh.read(MAX_CHARS)

            if fh.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return contents
    except Exception as e:
        return f"Error: {e}"
