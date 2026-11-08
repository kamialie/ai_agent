import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    abs_workdir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_workdir, directory))

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    if not os.path.commonpath([abs_workdir, target_dir]) == abs_workdir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    #return f'Success: "{directory}" is within the working directory'

    info = {}
    try:
        with os.scandir(target_dir) as it:
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
