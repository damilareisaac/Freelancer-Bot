import os
from actions import DomAction
import time


class LoginPage:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.action: DomAction = DomAction(driver)
        self.username: str = str(os.environ.get("username"))
        self.password: str = str(os.environ.get("password"))

        self.__login()
        print(self.driver.current_url)
        while self.driver.current_url != "https://www.freelancer.com/dashboard":
            time.sleep(3)
            print(self.driver.current_url)
            if (
                self.driver.current_url
                == "https://www.freelancer.com/users/limit-account/verification_center.php?w=f&ngsw-bypass="
            ):
                break
        print(self.driver.get_cookies())

    def __login(self) -> None:
        print("Logging in...")
        time.sleep(5)
        self.action.send_keys("//input[@id='emailOrUsernameInput']", self.username)
        self.action.send_keys("//input[@id='passwordInput']", self.password)
        # self.action.check_element("//button[@class='CheckboxLabel']")
        self.action.click("//button[@type='submit']")
        print("Logged in!")
