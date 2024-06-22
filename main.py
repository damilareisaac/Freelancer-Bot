from functools import partial
from dotenv import load_dotenv
import time
import os
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

    driver.add_cookie(
        {
            "name": "GETAFREE_USER_ID",
            "value": os.environ.get("GETAFREE_USER_ID"),
        }
    )
    driver.add_cookie(
        {
            "name": "GETAFREE_AUTH_HASH_V2",
            "value": os.environ.get("GETAFREE_AUTH_HASH_V2"),
        }
    )
    while True:
        project_links = BrowseProjects(driver).get_links()
        logger(to_console=True).info(f"Browsed {len(project_links)} projects")

        if len(project_links) >= 20:
            for link in project_links:
                action.switch_frame(link)
                time.sleep(5)
                try:
                    BidProjectPage(driver).bid_project(link)
                except Exception as e:
                    print(e)
                    logger().info(f"Unable to complete bid on {link}")
                    continue
        # wait 3 minutes before checking again
        time.sleep(180)
