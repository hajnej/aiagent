# main.py

import sys # Used for command line arguments
from pkg.calculator import Calculator # Import our custom Calculator class
from pkg.render import format_json_output # Import our formatter function


def main():
    calculator = Calculator()
    
    # Check if any arguments were passed (len is > 1 because the first arg is the script name)
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    # Join all arguments after the script name into a single string
    # e.g., ["3", "+", "5"] becomes "3 + 5"
    expression = " ".join(sys.argv[1:])
    try:
        # Calculate the result
        result = calculator.evaluate(expression)
        
        if result is not None:
            # Format and print the output
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        print(f"Error: {e}")


# Standard boilerplate to call main() when run directly
if __name__ == "__main__":
    main()
