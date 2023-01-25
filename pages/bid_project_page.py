from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from actions import AwaitAction
from pages.price_action import PriceAction
from pages.proposal_action import ProposalAction

from models.bids import Bids


class BidProjectPage:
    def __init__(self, driver: webdriver, wait, project_links) -> None:
        print("start project bid...")
        self.driver: webdriver = driver
        self.wait: WebDriverWait = wait
        self.links: list = project_links
        self.action: AwaitAction = AwaitAction(wait, self.driver)
        self.bid_btn_path: str = "//fl-button[@fltrackinglabel='PlaceBidButton']"
        self.nda_link_path: str = "//fl-link[@fltrackinglabel='NDALink']//a"

        self.execute()

    def execute(self) -> None:
        for link in self.links:
            self.action.switch_frame(link)
            self.bid_project(link)
            self.driver.close()
            self.action.switch_frame()

        self.driver.close()
        self.action.switch_frame()

    def bid_project(self, link) -> None:
        price_detail = self.get_price()
        if not price_detail:
            return
        price_action: PriceAction = PriceAction(price_detail)
        proposal_action: ProposalAction = ProposalAction(self.get_description())
        if (
            price_action.is_fit_for_bid()
            and self.has_bid_btn()
            and not self.has_complete_profile()
        ):
            if self.has_nda():
                self.sign_nda()

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
            self.action.send_keys("//textarea[@id='descriptionTextArea']", proposal)

            self.seal_bid()
            self.action.click(self.bid_btn_path)
            country, city, member_since = self.get_client_details()
            bids = Bids(
                id=self.get_project_id(),
                url=link,
                description=self.get_description(),
                price_detail=self.get_price(),
                proposal=proposal,
                skill=self.get_skill_tags(),
                country=country,
                city=city,
                member_since=member_since,
            )
            bids.save()
            print(f"Successful Bid on: {self.driver.current_url}")

    def sign_nda(self) -> None:
        try:
            el: WebElement = self.action.is_present(self.nda_link_path)
            el_link: str = el.get_attribute("href")
            self.action.switch_frame(el_link)
            self.action.click("//div[@id='container_agree_term']")
            self.action.click("//a[contains(text(),'Sign Agreement')]")
        except Exception as e:
            print(e)

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
        return self.action.get_text(
            "//fl-bit[@class='ProjectViewDetails-budget']//fl-text//div"
        )

    def get_description(self):
        return self.action.get_text("//fl-bit[@class='ProjectDescription']//span//span")

    def has_bid_btn(self) -> bool:
        return self.action.is_present(self.bid_btn_path)

    def has_complete_profile(self) -> bool:
        return self.action.find_element_(
            "//fl-card-header-title[contains(text(), 'Complete your profile')]"
        )

    def get_skill_tags(self):
        tags_el = self.action.get_all_elements(
            "//fl-tag[@fltrackinglabel='ProjectSkillTag']//fl-link//a"
        )
        tags = set([i.get_attribute("href").split("/")[-1] for i in tags_el])
        return ", ".join(tags)

    def get_project_id(self):
        project_id = self.action.get_text(
            " //fl-bit[@class='ProjectDetailsFooter-left']//fl-text//div[1]"
        )
        project_id = project_id.split(" ")[-1]
        return project_id

    def get_client_details(self):
        get_link = (
            lambda index: f"//app-employer-info/fl-card/fl-bit/fl-bit[2]/fl-list/fl-list-item[1]/fl-bit/fl-bit/fl-bit[1]/fl-bit[1]/fl-list/fl-list-item[{index}]/fl-bit/fl-bit/fl-bit/fl-bit/fl-bit/fl-text"
        )
        city = self.action.get_text(get_link(1))
        country = self.action.get_text(get_link(2))
        member_since = self.action.get_text(get_link(4))
        member_since = member_since.split(" ")[2:]
        member_since = " ".join(member_since)
        return country, city, member_since
