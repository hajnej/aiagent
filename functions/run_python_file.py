import subprocess
import os

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
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute
        # We run from the working_directory, so we pass the file_path relative to it.
        # file_path argument provided to this function is already relative to working_directory.
        command = ["python", file_path] + args
        
        result = subprocess.run(
            command,
            cwd=working_directory_absolute_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []
        
        output_parts.append(f"STDOUT: {result.stdout}")
        output_parts.append(f"STDERR: {result.stderr}")
        
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
            
        if not result.stdout and not result.stderr:
            return "No output produced"
            
        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Timeout expired"
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
