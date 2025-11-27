import sys

def all_stocks():
    COMPANIES = {
            'Apple': 'AAPL',
            'Microsoft': 'MSFT',
            'Netflix': 'NFLX',
            'Tesla': 'TSLA',
            'Nokia': 'NOK'
            }
    STOCKS = {
            'AAPL': 287.73,
            'MSFT': 173.79,
            'NFLX': 416.90,
            'TSLA': 724.88,
            'NOK': 3.37
            }

    if len(sys.argv) != 2:
        return

    input_string = sys.argv[1].strip()
    expressions = input_string.split(',')

    if ' ' in expressions or '' in expressions:
        return

    for expression in expressions:
        expression = expression.strip()

        if expression.upper() in STOCKS:
            ticker = expression.upper()
            company = None
            for key, value in COMPANIES.items():
                if value == ticker:
                    company = key
                    break
            print(f"{ticker} is a ticker symbol for {company}")
        elif expression.capitalize() in COMPANIES:
            company = expression.capitalize()
            ticker = COMPANIES[company]
            stock_price = STOCKS[ticker]
            print(f"{company} stock price is {stock_price}")
        else:
            print(f"{expression} is an unknown company or an unknown ticker symbol")

if __name__ == '__main__':
    all_stocks()
