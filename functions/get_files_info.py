import os

from functions.helpers import get_target_path

# directory parameter is a relative path, but need to make sure it doesn't go
# outside of working directory.
def get_files_info(working_directory: str, directory: str = ".") -> str:
    target = get_target_path(working_directory, directory)
    if not target:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'

    info = {}
    try:
        with os.scandir(target) as it:
            for entry in it:
                info[entry.name] = {
                    "size": entry.stat(follow_symlinks=False).st_size,
                    "is_dir": entry.is_dir(follow_symlinks=False)
                }
    except Exception as e:
        return f"Error: {e}"

    info_str = []
    for item, info in info.items():
        info_str.append(f"- {item}: file_size={info["size"]} bytes, is_dir={info["is_dir"]}")

    return "\n".join(info_str)
