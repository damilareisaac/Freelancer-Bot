ISOLATED_CURRENT = ["INR"]


class PriceAction:
    def __init__(self, price: str) -> None:
        self.is_hourly: bool = False
        self.price = price
        self.has_plus: bool = False
        (self.lower, self.upper, self.currency) = self.__preprocessed()

    def __preprocessed(self):
        if "per hour" in self.price:
            self.price: str = self.price.replace("per hour", "").strip()
            self.is_hourly = True
        self.price = self.price.replace(",", "")[1:].strip()
        if "+" in self.price:
            self.has_plus = True
            self.price = self.price.replace("+", "")
            left = 0
            right = self.price
        else:
            left, right = self.price.split("–")
        upper, currency = right.strip().split(" ")
        lower = int(float(left))
        upper = int(float(upper))
        return lower, upper, currency

    def get_currency(self) -> str:
        return self.currency

    def get_amount(self) -> int:
        return self.upper

    def get_timeline(self) -> str:
        period: int = int(self.upper / 60)
        if period < 1:
            return "1"
        if 30 < period < 60:
            return "30"
        if period > 100:
            return "100"
        return str(period)

    def is_fit_for_bid(self) -> bool:
        least_amount: int = 150
        if self.is_hourly:
            least_amount = 20
        currency_allowed: bool = self.currency not in ISOLATED_CURRENT
        fit = currency_allowed and self.upper >= least_amount
        return fit
