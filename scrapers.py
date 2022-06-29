import asyncio
import json

import nest_asyncio
import requests
from bs4 import BeautifulSoup
from pyppeteer import launch


class RadioGardenScraper(object):
    def __init__(self):
        self.api_endpoint = "https://radio.garden/api/ara"

    def get_places_list(self):
        return json.loads(
            requests.get(self.api_endpoint + "/content/places").content
        )["data"]["list"]

    def get_stations_list(self, place):
        # RadioGarden's API only outputs the first 5 stations for each place
        if place["size"] <= 5:
            return self.get_station_list_from_api(place["id"])
        # When the place size is > 5, we scrap the webpage to extract the links to all stations
        else:
            return self.get_station_list_from_html(place["title"], place["id"])

    def get_radio_stream_url(self, station_id):
        try:
            return requests.head(
                self.api_endpoint + "/content/listen/" + station_id + "/channel.mp3",
                allow_redirects=True
            ).url
        except:
            return self.api_endpoint + "/content/listen/" + station_id + "/channel.mp3",

    def get_station_list_from_api(self, place_id):
        return json.loads(
            requests.get(self.api_endpoint + "/content/page/" + place_id).content
        )["data"]["content"][0]["items"]

    def get_station_list_from_html(self, place_name, place_id):
        nest_asyncio.apply()

        station_names = []
        station_ids = []

        html = asyncio.get_event_loop().run_until_complete(
            self.get_place_html(place_name, place_id)
        )
        soup = BeautifulSoup(html, features="html.parser")
        for button in soup.find_all("div", {"class": "_title_blcjy_152"}):
            station_names.append(button.get_text())
        for link in soup.find_all("a", {"class": "_linkContainer_blcjy_13"}):
            try:
                station_ids.append(link["data-jest-href"])
            except:
                station_ids.append("")
        return [{"title": data[0], "href": data[1]} for data in list(zip(station_names, station_ids))]

    @staticmethod
    async def get_place_html(place_name, place_id):
        browser = await launch(headLess=False)
        page = await browser.newPage()
        await page.goto(f"https://radio.garden/visit/{place_name.lower()}/{place_id}/channels")
        await page.click('body')
        await page.waitForNavigation({"waitUntil": "networkidle0"})
        html = await page.content()
        return html
