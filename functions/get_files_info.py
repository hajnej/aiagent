import os # Standard library for file system operations

def get_files_info(working_directory, directory="."):
  """
  List files and directories within a specified path.
  """
  # Construct the full path to the directory we want to list
  directory_relative_path = os.path.join(working_directory, directory)
  
  # Resolve to absolute paths for security checks
  directory_absolute_path = os.path.abspath(directory_relative_path)
  working_directory_absolute_path = os.path.abspath(working_directory)
  
  # Check if the target is actually a directory
  if not os.path.isdir(directory_absolute_path):
    return f'Error: "{directory}" is not a directory'
    
  # Security Check: Ensure the target directory is inside the allowed working directory
  # We append os.sep (separator) to ensure we don't match partial directory names
  if not (directory_absolute_path + os.sep).startswith(working_directory_absolute_path + os.sep):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
  try:
    files_info = []
    # os.listdir returns a list of names in the directory (not full paths)
    for file in os.listdir(directory_absolute_path):
      # Create the full path to inspect the file properties
      filename = os.path.join(directory_absolute_path, file)
      
      # Get file size in bytes
      size = os.path.getsize(filename)
      
      # Check if it is a directory or a file
      is_dir = os.path.isdir(filename)
      
      # Format the info into a string and add to our list
      files_info.append(f'- {file}: file_size={size} bytes, is_dir={is_dir}')
      
    # Join all lines with newline characters to create the final output string
    return '\n'.join(files_info)
    
  except Exception as e:
    return f'Error: {str(e)}'
