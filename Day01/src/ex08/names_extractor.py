import sys

def extract_names(file_path):
    try:
        with open(file_path, 'r') as file:
            emails = file.read().splitlines()

        data = []
        for email in emails:
            if '@' in email and '.' in email:
                name, domain = email.split('@')
                if domain == 'corp.com':
                    first_name, last_name = name.split('.')
                    first_name = first_name.capitalize()
                    last_name = last_name.capitalize()
                    data.append((first_name, last_name, email))

        with open('employees.tsv', 'w') as output_file:
            output_file.write('Name\tSurname\tE-mail\n')
            for first_name, last_name, email in data:
                output_file.write(f"{first_name}\t{last_name}\t{email}\n")

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 names_extractor.py <file_path>")
    else:
        extract_names(sys.argv[1])

