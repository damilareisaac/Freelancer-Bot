from functools import partial
import os
from actions import DomAction
import time

from logs import get_logger

logger = partial(get_logger, __name__)

class LoginPage:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.action: DomAction = DomAction(driver)
        self.username: str = str(os.environ.get("username"))
        self.password: str = str(os.environ.get("password"))

        self.__login()
        
        logger(to_console=True).info(self.driver.current_url)
        while self.driver.current_url != "https://www.freelancer.com/dashboard":
            time.sleep(3)
            logger(to_console=True).info(self.driver.current_url)
            if (
                self.driver.current_url
                == "https://www.freelancer.com/users/limit-account/verification_center.php?w=f&ngsw-bypass="
            ):
                break
        logger(to_console=True).info(self.driver.get_cookies())

    def __login(self) -> None:
        logger(to_console=True).info("Logging in...")
        time.sleep(5)
        self.action.send_keys("//input[@id='emailOrUsernameInput']", self.username)
        self.action.send_keys("//input[@id='passwordInput']", self.password)
        self.action.click("//button[@type='submit']")
        logger(to_console=True).info("Logged in!")
