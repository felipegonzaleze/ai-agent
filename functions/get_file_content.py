import os
from google.genai import types
from config.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(full_path)

    if not abs_target_file.startswith(abs_working_dir): return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_target_file): return f'Error: "{file_path}" is not a regular file'

    try:
        with open(abs_target_file, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS - 1]
                return file_content_string, f"File '{file_path}' truncated at 10000 characters"
            return file_content_string
    except Exception as e:
        return f"Error reading file {e}"

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Gets the content in the specified path file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file content, relative to the working directory. If not provided do nothing"
                )
            }
        )
    ) 
