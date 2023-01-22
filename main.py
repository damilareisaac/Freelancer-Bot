import os
import time
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from bot.driver_context import DriverContext
from bot.pages.bid_project_page import BidProjectPage
from bot.pages.login_page import LoginPage
from bot.pages.browse_projects_page import BrowseProjects

load_dotenv("bot/.env")
username: str = str(os.environ.get("username"))
password: str = str(os.environ.get("password"))
TIMEOUT: int = 10

with DriverContext() as driver:
    wait: WebDriverWait = WebDriverWait(driver, TIMEOUT)
    driver.get("https://freelancer.com/login")
    LoginPage(
        driver,
        wait,
        dict(username=username, password=password),
    )
    while True:
        project_links: list[str] = BrowseProjects(driver, wait).get_links()
        BidProjectPage(driver, wait, project_links)
        time.sleep(120)
