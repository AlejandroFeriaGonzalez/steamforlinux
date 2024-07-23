import requests
from bs4 import BeautifulSoup
from models import models


def fetch_operating_system_requirements(gameId) -> models.GameRequirements:
    base_url = "https://store.steampowered.com/app/{gameId}"
    url = base_url.format(gameId=gameId)
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    title_element = soup.find("div", class_="apphub_AppName")
    title = title_element.text if title_element else "Unknown"

    os_requirements = soup.find("div", class_="sysreq_tabs")
    if not os_requirements:
        return models.GameRequirements(game_title=title, os_requirements=["Not available"])

    os_requirements = os_requirements.find_all("div", class_="sysreq_tab")
    os_requirements = [os.text.strip() for os in os_requirements]
    return models.GameRequirements(game_title=title, os_requirements=os_requirements)
