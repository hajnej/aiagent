import os

def get_files_info(working_directory, directory="."):
  directory_relative_path = os.path.join(working_directory, directory)
  directory_absolute_path = os.path.abspath(directory_relative_path)
  working_directory_absolute_path = os.path.abspath(working_directory)
  if not os.path.isdir(directory_absolute_path):
    return f'Error: "{directory}" is not a directory'
  if not (directory_absolute_path + os.sep).startswith(working_directory_absolute_path + os.sep):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  try:
    files_info = []
    for file in os.listdir(directory_absolute_path):
      filename = os.path.join(directory_absolute_path, file)
      size = os.path.getsize(filename)
      is_dir = os.path.isdir(filename)
      files_info.append(f'- {file}: file_size={size} bytes, is_dir={is_dir}')
    return '\n'.join(files_info)
  except Exception as e:
    return f'Error: {str(e)}'
