import os

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