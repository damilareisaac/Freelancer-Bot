from functools import partial
from dotenv import load_dotenv
import time

from actions import DomAction
from context import DriverContext
from logs import get_logger
from pages.bid_project_page import BidProjectPage
from pages.browse_projects_page import BrowseProjects

load_dotenv(".env")


logger = partial(get_logger, __name__)


with DriverContext() as driver:
    driver.get("https://freelancer.com")
    action = DomAction(driver)

    driver.add_cookie({"name": "GETAFREE_USER_ID","value": "11122738"})
    driver.add_cookie(
        {
            "name": "GETAFREE_AUTH_HASH_V2",
            "value": "IxxJA8hhCirxtL0nascvqx7Gdi9XChYBEHmW%2F2C%2F%2FLw%3D",
        }
    )
    while True:
        browsed_link = BrowseProjects(driver).get_links()
        logger(to_console=True).info(f"Browsed {len(browsed_link)} projects")

        if len(browsed_link) > 0:
            for link in browsed_link:
                action.switch_frame(link)
                time.sleep(5)
                try:
                    BidProjectPage(driver).bid_project(link)
                except Exception:
                    logger(to_console=True).info(f"Unable to complete bid on {link}")
                    continue
        time.sleep(120)
