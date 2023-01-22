from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from bot.actions import AwaitAction
from bot.pages.price_action import PriceAction
from bot.pages.proposal_action import ProposalAction
import time


class BidProjectPage:
    def __init__(self, driver: webdriver, wait, project_links) -> None:
        print("start project bid...")
        self.driver: webdriver = driver
        self.wait: WebDriverWait = wait
        self.links: list = project_links
        self.action: AwaitAction = AwaitAction(wait, self.driver)
        self.bid_btn_path: str = "//fl-button[@fltrackinglabel='PlaceBidButton']"
        self.nda_link_path: str = "//fl-link[@fltrackinglabel='NDALink']//a"
        self.ip_link_path: str = "//fl-link[@fltrackinglabel = 'IPAgreementLink']"

        self.execute()

    def execute(self) -> None:
        for link in self.links:
            self.action.switch_frame(link)
            self.bid_project()
            self.driver.close()
            self.action.switch_frame()
        self.driver.close()
        self.action.switch_frame()

    def bid_project(self) -> None:
        price_action: PriceAction = PriceAction(self.get_price())
        proposal_action: ProposalAction = ProposalAction(self.get_description())
        if price_action.is_fit_for_bid() and self.has_bid_btn():
            if self.has_nda():
                self.sign_nda()

            if self.has_ipa():
                print(f"IP agreement in {self.driver.current_url}")

            self.action.send_bid_amt(price_action.get_amount())

            if not price_action.is_hourly:
                self.action.send_keys(
                    "//input[@id='periodInput']", price_action.get_timeline()
                )
            proposal = str(
                f"""\
                Hi there!
                {proposal_action.get_proposal().strip()}
                Kind regards,
                Isaac
                """
            ).strip()
            print(proposal)
            self.action.send_keys("//textarea[@id='descriptionTextArea']", proposal)

            self.seal_bid()
            self.action.click(self.bid_btn_path)
            time.sleep(2)
            print(f"Successful Bid on: {self.driver.current_url}")

    def sign_ipa(self) -> None:
        ip_buttons: list[WebElement] = self.action.get_all_elements(
            "//fl-link[@fltrackinglabel='IPAgreementLink']"
        )
        for item in ip_buttons:
            try:
                item.click()
            except Exception:
                pass
        self.action.switch_frame()

    def sign_nda(self) -> None:
        try:
            el: WebElement = self.action.is_present(self.nda_link_path)
            el_link: str = el.get_attribute("href")
            self.action.switch_frame(el_link)
            self.action.click("//div[@id='container_agree_term']")
            self.action.click("//a[contains(text(),'Sign Agreement')]")
        except Exception as e:
            print(e)

    def has_ipa(self) -> bool:
        return self.action.find_element_(self.ip_link_path)

    def has_nda(self) -> bool:
        return self.action.find_element_(self.nda_link_path)

    def seal_bid(self) -> None:
        sealed: list[WebElement] = self.action.get_all_elements(
            "//fl-upgrade-tag[@data-upgrade-type='sealed']"
        )
        for item in sealed:
            try:
                item.click()
            except Exception:
                pass

    def get_price(self) -> str:
        price: WebElement = self.action.is_present(
            "//fl-bit[@class='ProjectViewDetails-budget']//fl-text//div"
        )
        return price.text

    def get_description(self):
        element: WebElement = self.action.is_present(
            "//fl-bit[@class='ProjectDescription']//span//span"
        )
        if element:
            return element.text

    def has_bid_btn(self) -> bool:
        return self.action.find_element_(self.bid_btn_path)
