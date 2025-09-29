import requests
from decimal import Decimal

class Currency:
    def all_rates(self):
        url = "https://api.currencyfreaks.com/latest?apikey=bd594ac932434551b038eb2a9987f015"
        response = requests.get(url)
        data = response.json()
        rates = {code: Decimal(rate) for code, rate in data["rates"].items()}
        return rates

    def list_currencies(self):
        return list(self.all_rates())

    def convert(self, amount, currency_have, currency_want):
        rates = self.all_rates()
        rate_have = rates.get(currency_have.upper())
        rate_want = rates.get(currency_want.upper())
        amount_usd = amount / rate_have
        amount_convert = amount_usd * rate_want
        return amount_convert.quantize(Decimal("0.01"))