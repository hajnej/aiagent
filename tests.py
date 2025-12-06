from functions.get_file_content import get_file_content

def main():
    print('get_file_content("calculator", "main.py"):')
    result = get_file_content("calculator", "main.py")
    print(result)
    print()

    print('get_file_content("calculator", "pkg/calculator.py"):')
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)
    print()

    print('get_file_content("calculator", "/bin/cat"):')
    result = get_file_content("calculator", "/bin/cat")
    print(result)
    print()

    print('get_file_content("calculator", "pkg/does_not_exist.py"):')
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)

if __name__ == "__main__":
    main()
