from bot.actions import AwaitAction
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


class BrowseProjects:
    def __init__(self, driver: webdriver, wait: WebDriverWait) -> None:
        print("Browsing projects...")
        self.driver: webdriver = driver
        self.wait: WebDriverWait = wait
        self.action: AwaitAction = AwaitAction(wait, self.driver)
        self.action.switch_frame("https://www.freelancer.com/search/projects")

    def get_links(self) -> list[str]:
        projects_tag: list[WebElement] = self.action.get_all_elements(
            "//fl-project-contest-card/parent::a | //a[@class='search-result-link']"
        )
        return [str(el.get_attribute("href")) for el in projects_tag]
