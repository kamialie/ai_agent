import os

def get_target_path(workdir: str, target: str) -> str | None:
    abs_workdir = os.path.abspath(workdir)
    abs_target = os.path.normpath(os.path.join(abs_workdir, target))

    if not os.path.commonpath([abs_workdir, abs_target]) == abs_workdir:
        return None
    return abs_target
