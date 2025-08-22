from google.genai import types
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_name, verbose=False):
    
    print(f"Calling function: {function_name.name}({function_name.args})") if verbose else print(f" - Calling function: {function_name.name}")

    functions_dictionary = {
        "get_file_content" : get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    kwargs = dict(function_name.args)
    kwargs['working_directory'] = './calculator'

    if function_name.name not in functions_dictionary:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name.name,
                    response={"error": f"Unknown function: {function_name.name}"}
                )
            ]
        )
    
    result = functions_dictionary[function_name.name](**kwargs)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name.name,
                response={"result": result}
            )
        ]
    )