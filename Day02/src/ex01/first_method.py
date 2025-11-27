class Research:
    def file_reader(self):
        with open("../data.csv", "r", encoding='utf-8') as file:
            return file.read().strip()

if __name__ == "__main__":
    research = Research()
    print(research.file_reader())
