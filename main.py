import time
from dotenv import load_dotenv
from context import DriverContext
from pages.bid_project_page import BidProjectPage
from pages.browse_projects_page import BrowseProjects

load_dotenv(".env")

import logging
import socket
from logging.handlers import SysLogHandler


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


syslog = SysLogHandler(address=("logs2.papertrailapp.com", 15222))
syslog.addFilter(ContextFilter())
format = "%(asctime)s %(hostname)s %(funcName)s %(lineno)d : %(message)s"
formatter = logging.Formatter(format, datefmt="%b %d %H:%M:%S")
syslog.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(syslog)
logger.setLevel(logging.INFO)


with DriverContext() as driver:
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
            "value": "IxxJA8hhCirxtL0nascvqx7Gdi9XChYBEHmW%2F2C%2F%2FLw%3D",
            "path": "/",
            "domain": "www.freelancer.com",
            "secure": True,
            "httpOnly": False,
            "sameSite": "None",
        }
    )
    driver.refresh()
    while True:
        browsed_link: list[str] = BrowseProjects(driver).get_links()
        logging.info(f"{len(browsed_link)} Available")
        print(f"{len(browsed_link)} Available")
        if len(browsed_link) > 0:
            BidProjectPage(driver, browsed_link)
        time.sleep(300)
