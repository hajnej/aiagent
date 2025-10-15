import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Parse args, return user prompt and verbosity
def parse_args(args):
    if not args:
            print("AI Code Assistant")
            print('\nUsage: python main.py "your prompt here" [--verbose]')
            print('Example: python main.py "How do I build a calculator app?"')
            sys.exit(1)

    # Parse --verbose flag
    verbose = False
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    user_prompt = " ".join(args)

    return user_prompt, verbose

def generate_response(user_prompt, verbose):
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)

def main():
    args = sys.argv[1:]

    user_prompt, verbose = parse_args(args)
    generate_response(user_prompt, verbose)

if __name__ == "__main__":
    main()
