from functools import partial
from actions import DomAction
from selenium.webdriver.remote.webelement import WebElement
import time

from logs import get_logger

logger = partial(get_logger, __name__)

class BrowseProjects:
    def __init__(self, driver) -> None:
        logger(to_console=True).info("Browsing projects...")
        self.driver = driver
        self.action: DomAction = DomAction(self.driver)
        self.action.switch_frame("https://www.freelancer.com/search/projects")
    

    def get_links(self):
        return self.action.get_links("//fl-project-contest-card/parent::a | //a[@class='search-result-link']")
    
    def get_prices(self):
        prices_el: list[WebElement] = []
        while True:
            prices_el = self.action.get_all_elements(
                "//fl-text[@class='AverageBid-amount']/div | //fl-upgrade-tag[@class='Sealed']",
            )
            time.sleep(3)
            if prices_el:
                break
        result = ["" if "sealed" in el.text.lower() else el.text for el in prices_el]
        return result