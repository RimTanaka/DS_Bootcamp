class Must_read:
    with open("../data.csv", "r") as file:
        for line in file:
            print(line.strip())
