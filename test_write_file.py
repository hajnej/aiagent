from functions.write_file import write_file

def main():
    # Test case 1: Write to a new file
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    # Test case 2: Overwrite an existing file (or write to a subdirectory)
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    # Test case 3: Attempt to write outside the working directory
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

if __name__ == "__main__":
    main()
