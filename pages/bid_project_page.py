import logging
from selenium.webdriver.remote.webelement import WebElement

from actions import DomAction, PriceAction, ProposalAction

from models.bids import Bids
import time


class BidProjectPage:
    def __init__(self, driver, project_links) -> None:
        self.driver = driver
        self.links: list = project_links
        self.action: DomAction = DomAction(self.driver)
        self.bid_btn_path: str = "//fl-button[@fltrackinglabel='PlaceBidButton']"
        self.nda_link_path: str = "//fl-link[@fltrackinglabel='NDALink']//a"

        self.execute()

    def execute(self) -> None:
        for link in self.links:
            self.action.switch_frame(link)
            time.sleep(5)  # wait is very important
            self.bid_project(link)

    def bid_project(self, link) -> None:
        price_detail = self.get_price()
        if not price_detail:
            return
        price_action: PriceAction = PriceAction(price_detail)
        if (
            price_action.is_fit_for_bid()
            and self.action.is_present(self.bid_btn_path)
            and not self.action.is_present(
                "//fl-card-header-title[contains(text(), 'Complete your profile')]"
            )
        ):
            if self.action.is_present(self.nda_link_path):
                self.sign_nda()

            self.action.send_bid_amt(price_action.get_amount())

            if not price_action.is_hourly:
                self.action.send_keys(
                    "//input[@id='periodInput']", price_action.get_timeline()
                )
            proposal_action: ProposalAction = ProposalAction(
                self.get_description(),
            )
            proposal = str(
                f"""\
                Hi there!
                {proposal_action.get_proposal().strip()}
                Kind regards,
                Isaac
                """
            ).strip()
            self.action.send_keys(
                "//textarea[@id='descriptionTextArea']",
                proposal,
            )

            self.seal_bid()
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);",
            )
            self.action.click(self.bid_btn_path)
            time.sleep(3)
            # project_id = self.get_project_id()
            # self.save_to_db(
            #     link,
            #     proposal,
            #     project_id,
            # )
            logging.info(f"Successful Bid on: {link}")
            print(f"Successful Bid on: {link}")

    def save_to_db(self, link, proposal, id):
        country, city, member_since = self.get_client_details()
        try:
            bids = Bids(
                id=id,
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
        except Exception as e:
            logging.error(e)

    def sign_nda(self) -> None:
        if not self.action.is_present(self.nda_link_path):
            return
        try:
            el = self.action.find_element_(self.nda_link_path)
            el_link = el.get_attribute("href")
            self.action.switch_frame(el_link)
            self.action.click("//div[@id='container_agree_term']")
            self.action.click("//a[contains(text(),'Sign Agreement')]")
        except Exception as e:
            logging.error(e)

    def seal_bid(self) -> None:
        sealed: list[WebElement] = self.action.get_all_elements(
            "//fl-upgrade-tag[@data-upgrade-type='sealed']"
        )
        for item in sealed:
            try:
                item.click()
            except Exception:
                pass

    def get_price(self):
        return self.action.get_text(
            "//fl-bit[@class='ProjectViewDetails-budget']//fl-text//div"
        )

    def get_description(self):
        return self.action.get_text("//fl-bit[@class='ProjectDescription']//span//span")

    def get_skill_tags(self):
        tags_el = self.action.get_all_elements(
            "//fl-tag[@fltrackinglabel='ProjectSkillTag']//fl-link//a"
        )
        tags = set(
            [i.get_attribute("href").split("/")[-1] for i in tags_el],
        )
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
