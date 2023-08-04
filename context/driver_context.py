from functools import partial
from selenium.webdriver import Firefox, FirefoxOptions
# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.firefox.service import Service as FirefoxService

from arg_parser import InputArgParser
from logs import get_logger

logger = partial(get_logger, __name__)

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
        logger(to_console=True).info(f"Current Mode: {current_mode}")
        if InputArgParser.is_headless():
            options.add_argument("--headless")



        # self.driver = Firefox(service=FirefoxService(GeckoDriverManager().install()))

        self.driver: Firefox = Firefox(options=options)

        self.driver.maximize_window()

    def __enter__(self) -> Firefox:
        return self.driver

    def __exit__(self, exc_type, exc_value, trace) -> bool:
        if exc_type:
            logger().exception(f"{trace}")
        logger().info("Exiting driver context")
        return True
