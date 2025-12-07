# render.py

import json # Used for working with JSON (JavaScript Object Notation) data


def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    """
    Format the result as a JSON string.
    
    Args:
        expression: The math expression (e.g., "3 + 5")
        result: The calculated value
        indent: Number of spaces for indentation (pretty printing)
    """
    # If the result is a whole number (like 8.0), convert it to an integer (8)
    # This makes the output look cleaner
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    # Create a Python dictionary (key-value pairs)
    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    
    # json.dumps converts the Python dictionary into a JSON formatted string
    return json.dumps(output_data, indent=indent)
