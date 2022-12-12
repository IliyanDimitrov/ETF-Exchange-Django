import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token b6b5e1f7311e71d060c0fdfac7bb17cf42b0f26b',
}

def get_meta_data(ticker):
    url = 'https://api.tiingo.com/tiingo/daily/{}'.format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()

def get_price_data(ticker):
    url = 'https://api.tiingo.com/tiingo/daily/{}/prices'.format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()[0]