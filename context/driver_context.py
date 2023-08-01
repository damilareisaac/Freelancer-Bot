from selenium.webdriver import Firefox, FirefoxOptions

from arg_parser import InputArgParser


class DriverContext:

    """_summary_
    define a driver context with custom configuration options for the driver
    log execution context to logger on error or success.
    """


    def __init__(self) -> None:
        options = FirefoxOptions()
        options.add_argument("start-maximized")
        options.add_argument("--log-level=3")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        current_mode: str = (
            "headless" if InputArgParser.is_headless() else "with-header"
        )
        print(f"Current Mode: {current_mode}")
        if InputArgParser.is_headless():
            options.add_argument("--headless")



        self.driver: Firefox = Firefox(options=options)

        self.driver.maximize_window()

    def __enter__(self) -> Firefox:
        return self.driver

    def __exit__(self, exc_type, exc_value, trace) -> bool:
        print(f"{exc_type} {exc_value} {trace}")
        # TODO: Implement the logger on error or success. 
        #       Test current class
        return True
