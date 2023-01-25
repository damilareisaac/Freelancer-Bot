from selenium import webdriver

from arg_parser import InputArgParser

PATH: str = "/Users/isaacomolewa/Documents/Development/Freelancer-Bot/geckodriver"


class DriverContext:
    def __init__(self) -> None:
        self.is_headless = InputArgParser.is_headless()
        self.options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()

        self.options.add_argument("start-maximized")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

        print(self.is_headless)
        if self.is_headless:
            self.options.add_argument("--headless")
        self.driver: webdriver = webdriver.Firefox(
            executable_path=PATH, options=self.options
        )

    def __enter__(self) -> webdriver:
        print("creating a selenium agent")
        return self.driver

    def __exit__(self, exc_type, _, __) -> bool:
        if exc_type:
            print(exc_type)
        else:
            print("Completed")
            # self.driver.quit()
        return False
