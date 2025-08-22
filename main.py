import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from config.config import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages= [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
            ))

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"Response: {response.text}")
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        if response.function_calls:
            called_functions = response.function_calls
            print(called_functions)
            for func in called_functions:
                print(f"Calling function: {str(func.name)}({str(func.args)})")
            print(response.text)

if __name__ == "__main__":
    main()
