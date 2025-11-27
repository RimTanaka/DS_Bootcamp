import sys

def search_by_ticker():
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

    ticker_symbol = sys.argv[1].upper()

    if ticker_symbol in STOCKS:
        company_name = None

        for key, value in COMPANIES.items():
            if value == ticker_symbol:
                company_name = key
                break

        print(f"{company_name} {STOCKS[ticker_symbol]}")
    else:
        print("Unknown ticker")

if __name__ == '__main__':
    search_by_ticker()
