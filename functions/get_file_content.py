import os

from functions.get_valid_path import check_is_working_path


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Show the content of a file in a specified directory relative to the working directory, with a limit of 10,000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file whose content is to be retrieved, relative to the specified directory",
                }
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        is_working_path = check_is_working_path(working_directory, os.path.dirname(file_path))#

        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if not is_working_path:
            raise ValueError(
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_file_path):
            raise ValueError(f'Error: File not found or is not a regular file: "{file_path}"')

        with open(target_file_path, "r", encoding="utf-8") as file:
            file_content = file.read(10000)
            is_truncated = bool(file.read(1))

        if is_truncated:
            file_content += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content
        
    except ValueError as exc:
        return str(f'Error: {exc}')


