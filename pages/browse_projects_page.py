import logging
from actions import DomAction
from selenium.webdriver.remote.webelement import WebElement
import time


class BrowseProjects:
    def __init__(self, driver) -> None:
        print("Browsing projects...")
        logging.info("Browsing projects...")
        self.driver = driver
        self.action: DomAction = DomAction(self.driver)
        self.action.switch_frame("https://www.freelancer.com/search/projects")

    def get_links(self) -> list:
        prj_tag_els: list[WebElement] = []
        time.sleep(2)
        while True:
            prj_tag_els = self.action.get_all_elements(
                "//fl-project-contest-card/parent::a | //a[@class='search-result-link']"
            )
            time.sleep(3)
            if prj_tag_els:
                break
        prj_links: list[str] = [self.get_href(el) for el in prj_tag_els if el]
        prj_links = [i for i in prj_links if "{[{" not in i]
        return prj_links

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

    def get_href(self, element):
        try:
            return str(element.get_attribute("href"))
        except Exception as e:
            logging.error(e)
            return ""

    # def get_filtered(self):
    #     return [
    #         link
    #         for price, link in zip(self.prices, self.links)
    #         if Bids.filter(link) and PriceAction(price).is_fit_for_bid()
    #     ]
