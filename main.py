import pandas as pd
from tqdm import tqdm

from scrapers import RadioGardenScraper
from utils import open_df, save_df


FILE_NAME = "world_radio"
FILE_FORMAT = ["csv", "json", "parquet"][0]


def main():
    df_world_radio = open_df(FILE_NAME, FILE_FORMAT)
    places_saved = df_world_radio["place_name"].drop_duplicates().values

    radio_garden_scraper = RadioGardenScraper()
    places_list = radio_garden_scraper.get_places_list()

    idx, nb_places = 0, len(places_list)
    for place in places_list:
        print(f'Place #{idx}/{nb_places} ({place["title"]}) is size {place["size"]}')
        idx += 1

        # Skip the computations if the station of the current place are already saved in the .csv
        if place["title"] in places_saved:
            continue

        stations_list = radio_garden_scraper.get_stations_list(place)
        place_data = []
        for station in tqdm(stations_list):
            station_id = station["href"].split("/")[-1]
            place_data.append(
                {
                    "country": place["country"],
                    "place_name": place["title"],
                    "place_id": place["id"],
                    "location": place["geo"],
                    "station_name": station["title"],
                    "station_id": station_id,
                    "station_stream_url": radio_garden_scraper.get_radio_garden_stream_url(station_id)
                }
            )
        print([station["title"] for station in stations_list])

        # Save all the stations information of the current place
        df_world_radio = pd.concat([df_world_radio, pd.DataFrame(place_data)], ignore_index=True)
        save_df(df_world_radio, FILE_NAME, FILE_FORMAT)


if __name__ == '__main__':
    main()
