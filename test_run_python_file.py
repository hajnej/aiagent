from functions.run_python_file import run_python_file

def main():
    print("--- Test 1: Run main.py (Usage info) ---")
    print(run_python_file("calculator", "main.py"))
    print("\n")

    print("--- Test 2: Run main.py with args ---")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("\n")

    print("--- Test 3: Run tests.py ---")
    print(run_python_file("calculator", "tests.py"))
    print("\n")

    print("--- Test 4: Security - Outside directory ---")
    print(run_python_file("calculator", "../main.py"))
    print("\n")

    print("--- Test 5: Security - Nonexistent file ---")
    print(run_python_file("calculator", "nonexistent.py"))
    print("\n")

    print("--- Test 6: Security - Not a Python file ---")
    print(run_python_file("calculator", "lorem.txt"))
    print("\n")

if __name__ == "__main__":
    main()
