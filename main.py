"""
AI Code Assistant - A simple assistant using Google Gemini API.
"""
import sys  # Used to access command line arguments passed to the script
import os   # Used to interact with the operating system (e.g., reading environment variables)
from typing import Tuple # Used for type hinting (specifying what kind of data functions return)
from dotenv import load_dotenv # Used to load configuration from a .env file (keeps secrets safe)
from google import genai # The official Google Gen AI library
from google.genai import types # Specific data types from the library
from prompts import system_prompt # Import the system instruction
from functions.get_files_info import schema_get_files_info # Import the function schema

# Constants
# We define constants at the top level to make them easy to change later
MODEL_NAME = "gemini-2.5-flash"

# Define the tools available to the LLM
available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)


def print_usage() -> None:
    """Print usage information."""
    print("AI Code Assistant")
    print('\nUsage: python main.py "your prompt here" [--verbose]')
    print('Example: python main.py "How do I build a calculator app?"')


def parse_args(args: list[str]) -> Tuple[str, bool]:
    """
    Parse command line arguments.

    Args:
        args: List of command line arguments

    Returns:
        Tuple containing user prompt and boolean for verbose mode

    Raises:
        ValueError: If no arguments are provided
    """
    # Check if the list of arguments is empty
    if not args:
        print_usage()
        raise ValueError("No prompt provided")

    # Copy the list to avoid modifying the original list passed to the function
    # This is a good practice to prevent side effects
    args_copy = args.copy()

    # Check if the "--verbose" flag is present in the arguments
    verbose = "--verbose" in args_copy
    if verbose:
        # Remove the flag so it doesn't become part of the prompt text
        args_copy.remove("--verbose")

    # Join the remaining arguments into a single string to form the prompt
    user_prompt = " ".join(args_copy)

    # .strip() removes leading/trailing whitespace. If the result is empty, the prompt is invalid.
    if not user_prompt.strip():
        raise ValueError("Prompt cannot be empty")

    return user_prompt, verbose


def get_api_client() -> genai.Client:
    """
    Create and return a Gemini API client.

    Returns:
        Initialized Gemini API client

    Raises:
        ValueError: If API key is not set
    """
    # Load environment variables from a .env file into os.environ
    load_dotenv()
    
    # Retrieve the API key safely. It returns None if the key doesn't exist.
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Create a .env file with: GEMINI_API_KEY=your_key"
        )

    # Initialize and return the client using the key
    return genai.Client(api_key=api_key)


def generate_response(client: genai.Client, user_prompt: str, verbose: bool = False) -> None:
    """
    Generate and print AI response.

    Args:
        client: Gemini API client
        user_prompt: User's query
        verbose: Whether to print additional token information

    Raises:
        Exception: On API communication error
    """
    # Prepare the message in the format expected by the API
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    try:
        # Make the network call to Google's servers
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], # Register our defined tools
                system_instruction=system_prompt,
            ),
        )
        
        # Verify we got valid usage metadata back
        if not response.usage_metadata:
            raise RuntimeError("Failed API response")

        # If verbose mode is on, print details about token usage (cost related)
        if verbose:
            print(f"\n{'='*50}")
            print(f"Prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"{'='*50}\n")

        # Check if the model decided to call a function
        if response.function_calls:
            for fc in response.function_calls:
                print(f"Calling function: {fc.name} ({fc.args})")
        else:
            # Print the actual text response from the AI
            print(response.text)

    except Exception as e:
        # Re-raise the exception with a clear message so the main function can handle it
        raise Exception(f"API communication error: {str(e)}")


def main() -> None:
    """Main program function."""
    try:
        # sys.argv[0] is the script name (main.py), so we start from index 1 to get arguments
        args = sys.argv[1:]
        
        # Unpack the tuple returned by parse_args into two variables
        user_prompt, verbose = parse_args(args)

        client = get_api_client()
        generate_response(client, user_prompt, verbose)

    except ValueError as e:
        # Print expected errors (like missing args) to stderr
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1) # Exit with a non-zero status code to indicate failure
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


# This block ensures main() runs only if the file is executed directly (not imported)
if __name__ == "__main__":
    main()
