def to_dict():
    list_of_tuples = [
          ('Russia', '25'),
          ('France', '132'),
          ('Germany', '132'),
          ('Spain', '178'),
          ('Italy', '162'),
          ('Portugal', '17'),
          ('Finland', '3'),
          ('Hungary', '2'),
          ('The Netherlands', '28'),
          ('The USA', '610'),
          ('The United Kingdom', '95'),
          ('China', '83'),
          ('Iran', '76'),
          ('Turkey', '65'),
          ('Belgium', '34'),
          ('Canada', '28'),
          ('Switzerland', '26'),
          ('Brazil', '25'),
          ('Austria', '14'),
          ('Israel', '12')
          ]
    countries_dict = {}

    for country, number in list_of_tuples:
        if number in countries_dict:
            countries_dict[number].append(country)
        else:
            countries_dict[number] = [country]

    for numb in countries_dict.keys():
        for country in countries_dict[numb]:
            print(f"'{numb}' : '{country}'")



if __name__ == '__main__':
    to_dict()
