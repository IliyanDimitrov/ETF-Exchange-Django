import django_tables2 as tables

context = [
    {"price_open": "1.5"},
    {"price_high": "2"},
    {"price_low": "1.3"},
    {"price_open": "1.4"},
    {"ticker": "APPL"},
]

class EtfTable(tables.Table):
    ticker = tables.Column() 
    price_open = tables.Column()
    price_high = tables.Column()
    price_low = tables.Column()
    price_close = tables.Column()

