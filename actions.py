import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    ElementNotInteractableException,
    NoSuchElementException,
    ElementClickInterceptedException,
)


class AwaitAction:
    def __init__(self, wait, driver) -> None:
        self.wait: WebDriverWait = wait
        self.driver: webdriver = driver
        self.arg_click: str = "arguments[0].click()"
        self.action_chains: ActionChains = ActionChains(driver)

    def click(self, x_path) -> None:
        element: WebElement = self.is_present(x_path)
        if element:
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script(self.arg_click, element)
            except ElementNotInteractableException:
                pass

    def check_element(self, x_path) -> None:
        element: WebElement = self.is_present(x_path)
        if (
            element
            and element.get_attribute("checked") != "true"
            or element.get_attribute("checked") != "checked"
        ):
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script(self.arg_click, element)

    def is_present(self, x_path):
        try:
            element: WebElement = self.wait.until(
                EC.presence_of_element_located((By.XPATH, x_path))
            )
            return element
        except Exception:
            return False

    def find_element_(self, path) -> bool:
        try:
            element: WebElement = self.driver.find_element(by=By.XPATH, value=path)
            if element:
                return True
            return False
        except NoSuchElementException:
            return False

    def is_visible(self, x_path) -> bool:
        try:
            element: WebElement = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, x_path))
            )
            return element
        except Exception:
            print(x_path, "Not found")
            return False

    def search_keys(self, x_path, keys, _return=False) -> None:
        element: WebElement = self.is_present(x_path)
        if element:
            try:
                element.clear()
                element.send_keys(keys)
                if _return:
                    element.send_keys(Keys.ENTER)
            except Exception as e:
                pass
            time.sleep(0.5)

    def send_keys(self, x_path, keys, _return=False) -> None:
        element: WebElement = self.is_present(x_path)
        while element and element.get_attribute("value").strip() != keys.strip():
            try:
                element.clear()
                element.send_keys(keys)
                if _return:
                    element.send_keys(Keys.ENTER)
            except Exception as e:
                break

    def send_bid_amt(self, amount) -> None:
        element: WebElement = self.is_present("//input[@id='bidAmountInput']")
        try:
            count: int = 0
            while count < 10:
                element.send_keys(Keys.BACK_SPACE)
                count += 1
            element.send_keys(amount)
        except Exception as e:
            print(e, "occurred")

    def get_all_elements(self, x_path) -> list:
        try:
            elements: WebElement = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, x_path))
            )
            return elements
        except TimeoutException:
            print(f"{x_path} NOT FOUND")
            return []

    def get_text(self, x_path) -> str:
        element = self.is_present(x_path)
        result = "" if type(element) == bool else element.text.strip()  # type: ignore
        return result.strip()

    def switch_frame(self, xpath=None) -> None:
        if xpath:
            self.driver.execute_script(f"""window.open("{xpath}","_blank");""")
        self.driver.switch_to.window(self.driver.window_handles[-1])
