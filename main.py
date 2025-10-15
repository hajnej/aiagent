"""
AI Code Assistant - A simple assistant using Google Gemini API.
"""
import sys
import os
from typing import Tuple
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Constants
MODEL_NAME = "gemini-2.0-flash-001"


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
    if not args:
        print_usage()
        raise ValueError("No prompt provided")

    # Copy the list to avoid modifying the original
    args_copy = args.copy()

    # Parse --verbose flag
    verbose = "--verbose" in args_copy
    if verbose:
        args_copy.remove("--verbose")

    user_prompt = " ".join(args_copy)

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
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Create a .env file with: GEMINI_API_KEY=your_key"
        )

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
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages
        )

        if verbose:
            print(f"\n{'='*50}")
            print(f"Prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"{'='*50}\n")

        print(response.text)

    except Exception as e:
        raise Exception(f"API communication error: {str(e)}")


def main() -> None:
    """Main program function."""
    try:
        args = sys.argv[1:]
        user_prompt, verbose = parse_args(args)

        client = get_api_client()
        generate_response(client, user_prompt, verbose)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
