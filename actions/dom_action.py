from functools import partial
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

from config import timeout
from logs import get_logger


logger = get_logger(__name__)

class DomAction:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, timeout)
        self.arg_click: str = "arguments[0].click()"
        self.action_chains: ActionChains = ActionChains(driver)

    def is_present(self, x_path) -> WebElement | bool:
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, x_path)))
            return True
        except Exception:
            logger.exception(f"Element {x_path} is not present")
            return False
    
    
        
    def is_visible(self, x_path) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, x_path)))
            return True
        except Exception:
            logger.exception(f"Element {x_path} is not visible")
            return False
        
    def find_element(self, x_path) -> WebElement | None:
        if not self.is_present(x_path):
            return None
        return self.driver.find_element(by=By.XPATH, value=x_path)

    def click(self, x_path) -> None:
        if not self.is_present(x_path):
            return
        element = self.driver.find_element(by=By.XPATH, value=x_path)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(self.arg_click, element)
        except Exception:
            logger.exception(f"Element {x_path} is not clickable")

    def check_element(self, x_path) -> None:
        if not self.is_present(x_path):
            return
        element = self.driver.find_element(by=By.XPATH, value=x_path)
        if (element.get_attribute("checked") == "true"
            or element.get_attribute("checked") == "checked"):
                return
        try:
            element.click()
        except ElementClickInterceptedException:
            logger.exception(f"Element {x_path} is not clickable")
            self.driver.execute_script(self.arg_click, element)


    def search_keys(self, x_path, keys, _return=False) -> None:
        element = self.driver.find_element(by=By.XPATH, value=x_path)
        if not element:
            return
        try:
            element.clear()
            element.send_keys(keys)
            if _return:
                element.send_keys(Keys.ENTER)
        except Exception:
            logger.exception(f"Cannot send key to {x_path}")
        time.sleep(0.5)

    def send_keys(self, x_path, keys, _return=False) -> None:
        element = self.driver.find_element(by=By.XPATH, value=x_path)
        if not element:
            logger.info(f"Element with {x_path} not found")
            return
        while element.get_attribute("value").strip() != keys.strip():
            try:
                element.clear()
                element.send_keys(keys)
                if _return:
                    element.send_keys(Keys.ENTER)
            except Exception:
                logger.exception(f"Cannot send key to {x_path}")
                break

    def get_all_elements(self, x_path) -> list:
        try:
            return self.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, x_path)))
        except TimeoutException as e:
            logger.exception(e)
            return []

    def get_text(self, x_path) -> str:
        element = self.driver.find_element(by=By.XPATH, value=x_path)
        if not element:
            logger.info(f"Element/Text with {x_path} not found")
            return ""
        try:
            return element.text.strip()
        except Exception as e:
            logger.exception(e)
            return ""

    def switch_frame(self, url) -> None:
        self.driver.execute_script(f"""window.open("{url}","_self");""")

    def open_new_tab(self, url):
        self.driver.execute_script(f"""window.open("{url}","_blank");""")
        self.driver.switch_to.window(self.driver.window_handles[-1])

 
    
    def close_current_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])




    def send_bid_amt(self, amount) -> None:
        x_path = "//input[@id='bidAmountInput']"
        if not self.is_present(x_path):
            return
        element = self.driver.find_element(by=By.XPATH, value=x_path)
        try:
            count: int = 0
            while count < 10:
                element.send_keys(Keys.BACK_SPACE)
                count += 1
            element.send_keys(amount)
        except Exception as e:
            logger.exception(f"Unable to send bid amount {amount} for {x_path}")


    def get_links(self, path) -> list:
        start_time = time.time()
        prj_tag_els: list[WebElement] = []
        time.sleep(2)
        while True:
            prj_tag_els = self.get_all_elements(path)
            time.sleep(3)
            if prj_tag_els or time.time() - start_time > 10:
                logger.info(f"Timeout waiting for element in {path} to load")
                break
        prj_links: list[str] = [self.get_href(el) for el in prj_tag_els if el]
        prj_links = [i for i in prj_links if "{[{" not in i]
        return prj_links
    

    def get_href(self, element):
        try:
            return str(element.get_attribute("href"))
        except Exception as e:
            logger.error(e)
            return ""