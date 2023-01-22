from bot.actions import AwaitAction
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


class LoginPage:
    def __init__(
        self, driver: webdriver, wait: WebDriverWait, login_details: dict
    ) -> None:
        self.driver: webdriver = driver
        self.username: str = str(login_details["username"])
        self.password: str = str(login_details["password"])
        self.action: AwaitAction = AwaitAction(wait, self.driver)

        self.__login()
        while self.driver.current_url != "https://www.freelancer.com/dashboard":
            time.sleep(3)

    def __login(self) -> None:
        print("Logging in...")
        self.action.send_keys("//input[@id='emailOrUsernameInput']", self.username)
        self.action.send_keys("//input[@id='passwordInput']", self.password)
        # self.action.check_element("//button[@class='CheckboxLabel']")
        self.action.click("//button[@type='submit']")
