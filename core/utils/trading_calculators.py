
def calculate_bid_ask_spread(bid_price: float, ask_price: float) -> float:
    """
    Returns bid-ask spread given a bid and ask price

    Parameters:
        bid_price (float): price of bid
        ask_price (float): price of ask
    
    """
    if bid_price > ask_price:
        raise ValueError(f'bid_price {bid_price} is greater than ask_price {ask_price}')
    
    return float(ask_price - bid_price)