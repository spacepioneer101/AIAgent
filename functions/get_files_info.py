import os

#Notice that, in the declaration for the LLM, we don't even mention the working_directory parameter of the function! 
#We'll be passing that argument "from the outside," without the LLM agent knowing about it or being able to affect it.
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            raise ValueError(
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            )

        if not directory == "." and not os.path.isdir(target_dir):
            raise ValueError(f'Error: "{directory}" is not a directory')

        content_string = ""

        for file in os.listdir(target_dir):
            #name
            file_name = os.path.basename(file)

            #file size
            file_size = os.path.getsize(target_dir)

            #directory or not
            is_directory = os.path.isdir(file)

            content_string += f'"{file_name}": file_size={file_size} bytes, is_dir={is_directory}\n'

        return content_string
    except ValueError as exc:
        return str(f'Error: {exc}')