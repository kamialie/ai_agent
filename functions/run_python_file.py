import os
import sys
import subprocess

from functions.helpers import get_target_path

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    target = get_target_path(working_directory, file_path)
    if not target:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = [sys.executable, target]
        if args:
            command.extend(args)

        process = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        output = ""
        if process.returncode:
            output += f"Process exited with code {process.returncode}\n"

        out_count = len(process.stdout)
        err_count = len(process.stderr)
        if out_count == 0 and err_count == 0:
            output += "No output produced\n"
        else:
            if out_count:
                output += "STDOUT:\n"
                output += process.stdout
            if err_count:
                output += "STDERR:\n"
                output += process.stderr
        return output
    except ImportError as e:
        return f"Error: executing Python file: {e}"

