import requests
from stockexchange import env 

# Set required headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': env.TIINGO_TOKEN,
}

def get_meta_data(ticker):
    url = 'https://api.tiingo.com/tiingo/daily/{}'.format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()

def get_price_data(ticker):
    url = 'https://api.tiingo.com/tiingo/daily/{}/prices'.format(ticker)
    response = requests.get(url, headers=headers)
    try:
        return response.json()[0]
    except KeyError:
        return "API query limit has been reached"

def get_data_from_api():
    # Set API ETF tickers
    tickers = ['AAPL', 'GOOG', 'GOOGL', 'TSLA']
    # tickers = ['GOOG']

    # Create empty list to store data
    data = []

    # Loop through for all tickers
    for i in range(len(tickers)):
        # Make a request to the first API endpoint to get the price data
        price_endpoint = 'https://api.tiingo.com/tiingo/daily/{}/prices'.format(tickers[i])
        price_response = requests.get(price_endpoint, headers=headers)

        # Make a request to the second API endpoint to get the name data
        name_endpoint = 'https://api.tiingo.com/tiingo/daily/{}'.format(tickers[i])
        name_response = requests.get(name_endpoint, headers=headers)

        # Check for successful responses
        if price_response.status_code == 200 and name_response.status_code == 200:
            # Parse the responses as JSON
            price_data = price_response.json()[0]
            name_data = name_response.json()

            # Combine the data from the two responses
            combined_data = {
                'price': price_data,
                'name': name_data,
            }

            # Add the combined data to the list
            data.append(combined_data)

    # Return the data
    return data