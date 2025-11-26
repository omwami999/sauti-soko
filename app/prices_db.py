
PRICES = {
    "sukuma wiki": {"price": 45, "market": "Wakulima Market", "unit": "kg"},
    "nyanya": {"price": 80, "market": "Githurai", "unit": "kg"},
    "maharage": {"price": 120, "market": "Kawangware", "unit": "kg"},
    "mchele": {"price": 180, "market": "Mombasa", "unit": "kg"},
    "maandazi": {"price": 20, "market": "Kibera", "unit": "piece"},
}

def get_current_prices():
    return PRICES

def search_price(query: str):
    query = query.replace("bei ya", "").replace("bei", "").replace("ya", "").strip()
    for item in PRICES.keys():
        if item in query or any(word in query for word in item.split()):
            return item
    return None