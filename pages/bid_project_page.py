from functools import partial
from selenium.webdriver.remote.webelement import WebElement
from actions import DomAction, PriceAction, ProposalAction
from logs import get_logger
from models.bids import Bids
import time

logger = partial(get_logger, __name__)

class BidProjectPage:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.action: DomAction = DomAction(self.driver)
        self.bid_btn_path: str = "//fl-button[@fltrackinglabel='PlaceBidButton']"
        self.nda_link_path: str = "//fl-link[@fltrackinglabel='NDALink']//a"


    def bid_project(self, link) -> None:
        price_detail = self.get_price()
        if not price_detail:
            logger(to_console=True).info("No price details found")
            return
        price_action: PriceAction = PriceAction(price_detail)
        if (not price_action.is_fit_for_bid() or 
        not self.action.is_present(self.bid_btn_path) or 
        self.action.is_present("//fl-card-header-title[contains(text(), 'Complete your profile')]")
        ):
            
            return
       
        if self.action.is_present(self.nda_link_path):
            self.sign_nda()
            logger().info(f"SIGNED NDA for {link}")

        self.action.send_bid_amt(price_action.get_amount())

        if not price_action.is_hourly:
            self.action.send_keys(
                    "//input[@id='periodInput']", price_action.get_timeline()
            )
        
        proposal_action = ProposalAction()
        if not proposal_action.check_proposal_in_cache_for_link(link):
            description_text = self.get_description()
            proposal = str(
                f"""\
                Hi there!
                {proposal_action.get_proposal(description_text)}
                Kind regards,
                Isaac \
                """
            )
        else:
            proposal = proposal_action.check_proposal_in_cache_for_link(link)
        self.action.send_keys("//textarea[@id='descriptionTextArea']", proposal)

        self.seal_bid()
        self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);",
        )
        self.action.click(self.bid_btn_path)
        time.sleep(3)
        bid_logged = self.check_link_in_previous_bids_page(link)
        if bid_logged:
            logger(to_console=True).info(f"Successful Bid on: {link}")
            proposal_action.delete_proposal_from_cache(link)
        else:
            proposal_action.update_bid_cache(link, proposal)


    
    def check_link_in_previous_bids_page(self, link):
        self.action.open_new_tab("https://www.freelancer.com/manage/work/projects/open?query=&filter=All&quotesFilter=All&show=20&serviceOfferingsFilter=All")
        bid_links = self.action.get_links("//app-manage-project-title/fl-bit/fl-link/a")
        self.action.close_current_tab()
        return link in bid_links
        

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
            logger(to_console=True).error("Bid cannot be saved to database: %s" % e)

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
            logger().error("Unable to sign NDA")
            logger().exception(e)

    def seal_bid(self) -> None:
        sealed: list[WebElement] = self.action.get_all_elements(
            "//fl-upgrade-tag[@data-upgrade-type='sealed']"
        )
        for item in sealed:
            try:
                item.click()
            except Exception as e:
                logger().error("Unable to seal bid")
                logger().exception(e)

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
