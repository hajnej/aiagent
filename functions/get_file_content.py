import os # Standard library for operating system interactions (paths, files)
from google.genai import types # Import necessary types for function declaration
from config import MAX_CHARS # Import our limit constant

# Define the schema for the get_file_content function to be exposed to the LLM
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file within the working directory",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    """
    Read the content of a file within the working directory.

    Args:
        working_directory: The base directory to restrict access to
        file_path: Relative path to the file within working_directory

    Returns:
        String containing file content or error message
    """
    # Create absolute paths
    # os.path.join intelligently combines path components (handling slash/backslash differences)
    file_relative_path = os.path.join(working_directory, file_path)
    # os.path.abspath resolves relative paths (like '..') to a full path starting from root
    file_absolute_path = os.path.abspath(file_relative_path)
    working_directory_absolute_path = os.path.abspath(working_directory)

    # Check if file is within working directory boundaries
    # This prevents "path traversal attacks" where a user might try to access files outside the sandbox
    # e.g., "../../etc/passwd"
    # We add os.sep (directory separator) to ensure we match directory boundaries exactly
    if not (file_absolute_path + os.sep).startswith(working_directory_absolute_path + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if it's a regular file (not a directory or special file)
    if not os.path.isfile(file_absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # Read file content with limit
        # 'with open(...)' ensures the file is properly closed even if an error occurs
        # encoding="utf-8" is important for reading text files correctly
        with open(file_absolute_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

        # Check if file was truncated (if the content length equals our limit)
        if len(content) == MAX_CHARS:
            # Check if there's more content in the file
            f.seek(0, 2)  # Move the file cursor to the end of the file
            total_size = f.tell() # Get the current cursor position (which is the file size)
            
            # If the actual file size is larger than what we read, append a warning
            if total_size > MAX_CHARS:
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        # Catch any errors (like permission denied) and return them as a string
        return f"Error: {str(e)}"
