# World Radio Scraper
A script that scraps all the necessary informations about internet radios all around the world.

___

## APIs

- RadioGarden API : https://radio.garden/api

## Output data

### Format 
`csv` / `json` / `parquet`

### Columns 
Name | Type | Example | Description
--- | --- | --- | --- | 
country | string | France | Country of the radio | 
place_name | string | La Clusaz | Place (or city) of the radio | 
place_id | string | QP0Xzssl | RadioGarden's Id of the place | 
location | array | [6.423353, 45.904427] | Longitude & Latitude of the place | 
station_name | string | Radio Meuh | Name of the radio | 
station_id | string | dVSxCePq | RadioGarden's Id of the station |
station_stream_url | string | https://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3 | URL of the internet radio stream |
