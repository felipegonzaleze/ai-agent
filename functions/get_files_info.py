import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    full_path = os.path.join(working_directory, directory)
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(full_path)

    if not abs_target_dir.startswith(abs_working_dir): return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target_dir): return f'Error: "{directory}" is not a directory'

    try:
        files_info = []
        for file in os.listdir(abs_target_dir):
            filepath = os.path.join(abs_target_dir, file)
            file_size = os.path.getsize(filepath)
            file_is_dir = os.path.isdir(filepath)
            files_info.append(f"- {file}: file_size={file_size} bytes, is_dir={file_is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files{e}"
    
schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
                )
            }
        )
    )
