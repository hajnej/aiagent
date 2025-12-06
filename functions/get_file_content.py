import os
from config import MAX_CHARS

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
    file_relative_path = os.path.join(working_directory, file_path)
    file_absolute_path = os.path.abspath(file_relative_path)
    working_directory_absolute_path = os.path.abspath(working_directory)

    # Check if file is within working directory boundaries
    if not (file_absolute_path + os.sep).startswith(working_directory_absolute_path + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if it's a regular file
    if not os.path.isfile(file_absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # Read file content with limit
        with open(file_absolute_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

        # Check if file was truncated
        if len(content) == MAX_CHARS:
            # Check if there's more content
            f.seek(0, 2)  # Seek to end
            total_size = f.tell()
            if total_size > MAX_CHARS:
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"
