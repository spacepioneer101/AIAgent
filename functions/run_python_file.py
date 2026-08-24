import os, subprocess
from functions.get_valid_path import check_is_working_path

schema_run_python_file= {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a Python file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to be executed, relative to the specified directory",
                }
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        is_working_path = check_is_working_path(working_directory, os.path.dirname(file_path))#
    
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
        if not is_working_path == True:
            raise ValueError(
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )
    
        if os.path.isdir(target_file_path):
                raise ValueError(f'Error: Cannot write to "{file_path}" as it is a directory')

        if not os.path.isfile(target_file_path):
            raise ValueError(f'Error: "{file_path}" does not exist or is not a regular file')

        if not target_file_path.endswith(".py"):
            raise ValueError(f'Error: File "{file_path}" is not a Python file')

        command = ["python", target_file_path]

        if args is not None:
            command.extend(args)
        
        result = subprocess.run(command, check=True, cwd=working_dir_abs, text=True, capture_output=True, timeout=30)

        stdout = result.stdout
        stderr = result.stderr

        process_result = ""

        if result.returncode != 0:
            process_result += f"Error: Process exited with code " + {result.returncode}

        if len(stdout) == 0 and  len(stderr) == 0:
            process_result += f"No output produced"
        elif len(stdout) > 0:
            process_result += f"STDOUT: \n{stdout}\n"   
        elif len(stderr) > 0:
            process_result += f"STDERR: \n{stderr}\n"   


        return process_result
    except ValueError as exc:
        return str(f'Error: executing Python file: {exc}')
    