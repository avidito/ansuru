import os
import json
import requests

from bs4 import BeautifulSoup


script_dir = os.path.dirname(os.path.realpath(__file__))
pathname = os.path.join(script_dir, "manga_list.json")
with open(pathname, "r") as file:
    manga_list = json.loads(file.read())


def get_params(manga_id: str) -> list:
    params = None
    for manga in manga_list:
        if (manga.get("id") == manga_id):
            params = manga
            break
    
    if (params):
        return params
    else:
        raise KeyError(f"No manga with ID `{manga_id}`")
        
def get_scraper(scr: dict) -> callable:
    return {
        "mangabat": mangabat_scraper
    }[scr.get("name")]


# Scraper List
def mangabat_scraper(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()

    page = BeautifulSoup(response.text, features="html.parser")
    
    story_info = page.find(class_="panel-story-info").find(class_="story-info-right-extent").find_all("p")
    result = {
        "latest_dt" : story_info[0].find_all("span")[1].text,
        "latest_chp": story_info[3].find_all("span")[1].text,
        "latest_url": story_info[3].find_all("span")[1].a.get("href")
    }

    return result