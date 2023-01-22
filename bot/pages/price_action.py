ISOLATED_CURRENT: list[str] = ["INR"]


class PriceAction:
    def __init__(self, price: str) -> None:
        self.is_hourly: bool = False
        self.price = price
        (self.lower, self.upper, self.currency) = self.__preprocessed()

    def __preprocessed(self) -> tuple[int, int, str]:
        if "per hour" in self.price:
            self.price: str = self.price.replace("per hour", "").strip()
            self.is_hourly = True
        self.price = self.price.replace(",", "")[1:].strip()
        left, right = self.price.split("–")
        upper, currency = right.strip().split(" ")
        lower = int(float(left))
        upper = int(float(upper))
        return lower, upper, currency

    def get_currency(self) -> str:
        return self.currency

    def get_amount(self) -> int:
        return round(self.upper * 0.8)

    def get_timeline(self) -> str:
        period: int = int(self.upper / 60)
        return "1" if period < 1 else str(period)

    def is_fit_for_bid(self) -> bool:
        least_amount: int = 100
        if self.is_hourly:
            least_amount = 20
        currency_allowed: bool = self.currency not in ISOLATED_CURRENT
        return currency_allowed and self.upper >= least_amount
