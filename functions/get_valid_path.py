import os
from xmlrpc.client import Boolean

def check_is_working_path(working_directory: str, directory: str = ".") -> Boolean:
    try:

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            raise ValueError(
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            )

        if not os.path.isdir(target_dir):
            raise ValueError(f'Error: "{directory}" is not a directory')

        return True
    except ValueError as exc:
        return str(f'Error: {exc}')