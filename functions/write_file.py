import os

from functions.get_valid_path import check_is_working_path

schema_write_file= {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write content to a file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to be written, relative to the specified directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file"
                }
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
        try:
            is_working_path = check_is_working_path(working_directory, os.path.dirname(file_path))#

            working_dir_abs = os.path.abspath(working_directory)
            target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

            if not is_working_path == True:
                raise ValueError(
                    f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
                )

            if os.path.isdir(target_file_path):
                raise ValueError(f'Error: Cannot write to "{file_path}" as it is a directory')

            #Make sure that all parent directories of the file_path exist. 
            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

            with open(target_file_path, "w", encoding="utf-8") as file:
                file_content = file.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

        except ValueError as exc:
            return str(f'Error: {exc}')
