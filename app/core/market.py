# Simple hardcoded prices for MVP as per plan
MARKET_PRICES = {
    "soybean": 4800,
    "cotton": 6500,
    "pigeon pea": 7200,
    "gram": 5100
}

class MarketService:
    def get_price(self, crop: str):
        """Returns price per quintal."""
        crop = crop.lower()
        for k, v in MARKET_PRICES.items():
            if k in crop:
                return v
        return None

market_service = MarketService()
