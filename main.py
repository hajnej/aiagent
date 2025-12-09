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
from functions.get_files_info import schema_get_files_info, get_files_info # Import the function schema and implementation
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

# Constants
# We define constants at the top level to make them easy to change later
MODEL_NAME = "gemini-2.5-flash-lite"

# Define the tools available to the LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)

# Mapping of function names to their implementations
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


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


def call_function(function_call_part: types.FunctionCall, verbose: bool = False) -> types.Content:
    """
    Execute a function call from the model.

    Args:
        function_call_part: The function call object from the model
        verbose: Whether to print verbose output

    Returns:
        types.Content object containing the tool response
    """
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name} ({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Inject working directory
    function_args["working_directory"] = "./calculator"
    
    try:
        # Execute the actual function
        function_result = function_map[function_name](**function_args)
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
         return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing function: {str(e)}"},
                )
            ],
        )


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
        # Loop to allow for multiple turns (feedback loop)
        for _ in range(20):
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
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print(f"{'='*50}\n")

            # Append the model's response to the history
            # Iterate over candidates and add their content to messages
            if response.candidates:
                for candidate in response.candidates:
                     messages.append(candidate.content)

            # Check if the model decided to call a function
            if response.function_calls:
                tool_responses = []
                for fc in response.function_calls:
                    function_call_result = call_function(fc, verbose)
                    
                    # Check for response existence (as per instructions)
                    if not function_call_result.parts[0].function_response.response:
                        raise RuntimeError(f"Missing response for function call: {fc.name}")
                    
                    tool_responses.append(function_call_result.parts[0])
                    
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                
                # Create a message with the tool results and append to history
                # Role is 'user' for tool responses in this specific API usage pattern if 'tool' role isn't explicitly requested by the framework in a different way.
                # However, the task description says: "use the types.Content constructor to convert the list of responses into a message with role user, and append it to your messages."
                # NOTE: Usually tool responses have role='tool', but we follow instructions.
                # Wait, strictly following "message with role user" as per prompt instructions.
                # Actually, standard Gemini API expects role='user' or 'function' depending on version. 
                # The prompt explicitly says: "message with role user".
                
                # Re-reading: "use the types.Content constructor to convert the list of responses into a message with role user"
                # But wait, `function_call_result` parts are `types.Part.from_function_response`. 
                # These parts are usually associated with role 'tool'.
                # Let's verify if `types.Content(role="tool", ...)` is what is actually needed for the API to understand it's a tool response.
                # The instruction says "role user". I will follow the instruction but if it fails I might need to check.
                # Actually, looking at standard docs, it's usually `role='tool'`.
                # BUT, I will follow "message with role user" as per the explicit prompt text: "convert the list of responses into a message with role user".
                
                # Correction: The Part object itself contains the function response.
                messages.append(types.Content(role="user", parts=tool_responses))
                
                # Continue the loop to let the model process the tool output
                continue

            elif response.text:
                # Print the actual text response from the AI
                print(response.text)
                break
            
            else:
                 # No text and no function call?
                 break

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
