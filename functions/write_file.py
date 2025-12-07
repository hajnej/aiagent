import os # Standard library for file system operations

def write_file(working_directory, file_path, content):
    """
    Write content to a file within the working directory.

    Args:
        working_directory: The base directory to restrict access to
        file_path: Relative path to the file within working_directory
        content: The content to write to the file

    Returns:
        String confirming success or error message
    """
    try:
        # Create absolute paths to resolve relative segments like '..'
        file_relative_path = os.path.join(working_directory, file_path)
        file_absolute_path = os.path.abspath(file_relative_path)
        working_directory_absolute_path = os.path.abspath(working_directory)

        # Check if file is within working directory boundaries
        # os.path.commonpath returns the longest common sub-path.
        # If the file is inside the working directory, the common path must BE the working directory.
        if not os.path.commonpath([working_directory_absolute_path, file_absolute_path]) == working_directory_absolute_path:
             return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Write content to file
        # "w" mode opens the file for writing. It truncates the file first (deletes old content).
        # encoding="utf-8" ensures text is saved correctly.
        with open(file_absolute_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to {file_path} ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
