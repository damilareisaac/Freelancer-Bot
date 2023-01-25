import os
import time
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from driver_context import DriverContext
from models.bids import Bids
from pages.bid_project_page import BidProjectPage
from pages.login_page import LoginPage
from pages.browse_projects_page import BrowseProjects

load_dotenv(".env")
username: str = str(os.environ.get("username"))
password: str = str(os.environ.get("password"))
TIMEOUT: int = 10

with DriverContext() as driver:
    wait: WebDriverWait = WebDriverWait(driver, TIMEOUT)
    # driver.get("https://freelancer.com/login")
    # LoginPage(
    #     driver,
    #     wait,
    #     dict(username=username, password=password),
    # )
    driver.get("https://freelancer.com")
    driver.add_cookie(
        {
            "name": "GETAFREE_USER_ID",
            "value": "11122738",
            "path": "/",
            "domain": "www.freelancer.com",
            "secure": True,
            "httpOnly": False,
            "sameSite": "None",
        }
    )
    driver.add_cookie(
        {
            "name": "GETAFREE_AUTH_HASH_V2",
            "value": "oI2qeTdV73R8Mpb67rCzrLkauR3CReOMPZwCs5IrrjE%3D",
            "path": "/",
            "domain": "www.freelancer.com",
            "secure": True,
            "httpOnly": False,
            "sameSite": "None",
        }
    )
    driver.refresh()
    time.sleep(10)
    while True:
        project_links: list[str] = BrowseProjects(driver, wait).get_links()
        if len(project_links) > 0:
            filtered_link = Bids.filter(project_links)
            BidProjectPage(driver, wait, filtered_link)
        else:
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
        time.sleep(300)
