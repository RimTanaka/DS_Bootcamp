import sys

def search_by_key():
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

    company_name = sys.argv[1].capitalize()

    if company_name in COMPANIES:
        stock_symbol = COMPANIES[company_name]
        print(STOCKS[stock_symbol])
    else:
        print("Unknown company")

if __name__ == '__main__':
    search_by_key();
