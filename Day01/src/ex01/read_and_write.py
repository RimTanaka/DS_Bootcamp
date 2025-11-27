def read_and_write():
    with open('ds.csv', 'r', encoding='utf-8') as infile:
        data = infile.readlines()

    with open('ds.tsv', 'w', encoding='utf-8') as outfile:
        for line in data:
            result = []
            in_quotes = False
            for char in line:
                if char == '"':
                    in_quotes = not in_quotes
                if char == ',' and not in_quotes:
                    result.append('\t')
                else:
                    result.append(char)
            outfile.write(''.join(result))

if __name__ == '__main__':
    read_and_write()
