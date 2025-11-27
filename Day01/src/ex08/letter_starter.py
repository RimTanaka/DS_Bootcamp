import sys

def generate_letter(email):
    try:
        with open('employees.tsv', 'r') as file:
            lines = file.read().splitlines()

        headers = lines[0].split('\t')
        data = [line.split('\t') for line in lines[1:]]

        for entry in data:
            if entry[2] == email:
                name = entry[0]
                print(f"Dear {name}, welcome to our team. "
                      f"We are sure that it will be a pleasure to work with you. "
                      f"That’s a precondition for the professionals that our company hires.")
                return

        print(f"Email {email} not found in the records.")
    except FileNotFoundError:
        print("Error: File 'employees.tsv' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 letter_starter.py <email>")
    else:
        generate_letter(sys.argv[1])

