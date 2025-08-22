import os
from google.genai import types

def write_file(working_directory, file_path, content):

    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(full_path)

    if not abs_target_file.startswith(abs_working_dir): return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_target_file):
        try:
            os.makedirs(os.path.dirname(abs_target_file), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    
    if os.path.exists(abs_target_file):
        try:
            with open(full_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path} ({len(content)} characters written)'
        except Exception as e:
            return f"Error writing content to file: {e}"
        
schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Write or overwrite files.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file content, relative to the working directory."
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="Content to write or overwrite in the specified file path"
                )
            }
        )
    ) 
