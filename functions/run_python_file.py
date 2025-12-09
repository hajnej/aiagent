import subprocess # Used to run external commands (like 'python script.py')
import os # Standard library for file system operations
from google.genai import types # Import necessary types for function declaration

# Define the schema for the run_python_file function to be exposed to the LLM
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file securely within a constrained working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file within the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="List of command line arguments to pass to the script",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    """
    Execute a Python file securely within a constrained working directory.

    Args:
        working_directory: The base directory to restrict access to (and use as CWD)
        file_path: Relative path to the file within working_directory
        args: List of command line arguments to pass to the script

    Returns:
        String containing stdout, stderr, and status information
    """
    try:
        # Create absolute paths
        # Note: file_path is relative to working_directory
        file_relative_path = os.path.join(working_directory, file_path)
        file_absolute_path = os.path.abspath(file_relative_path)
        working_directory_absolute_path = os.path.abspath(working_directory)

        # 1. Security Check: Inside working directory
        if not os.path.commonpath([working_directory_absolute_path, file_absolute_path]) == working_directory_absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 2. Security Check: File exists
        if not os.path.isfile(file_absolute_path):
            return f'Error: File "{file_path}" not found.'

        # 3. Security Check: File extension
        # We only allow executing .py files for safety
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute
        # We run from the working_directory, so we pass the file_path relative to it.
        # This keeps imports working correctly (e.g. from pkg import ...)
        command = ["python", file_path] + args
        
        # subprocess.run executes the command and waits for it to finish
        result = subprocess.run(
            command,
            cwd=working_directory_absolute_path, # Set the Current Working Directory
            capture_output=True, # Capture what the script prints (stdout/stderr)
            text=True, # Decode output as text (strings) instead of bytes
            timeout=30 # Stop the process if it takes longer than 30 seconds
        )

        output_parts = []
        
        # Collect Standard Output (normal print statements)
        output_parts.append(f"STDOUT: {result.stdout}")
        # Collect Standard Error (error messages)
        output_parts.append(f"STDERR: {result.stderr}")
        
        # Check if the script failed (non-zero exit code)
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
            
        # Handle case where nothing was printed
        if not result.stdout and not result.stderr:
            return "No output produced"
            
        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Timeout expired"
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
