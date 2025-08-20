import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages= [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    response = client.models.generate_content(model="gemini-2.0-flash-001",contents=messages,config=types.GenerateContentConfig(system_instruction=system_prompt))

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"Response: response.text")
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
