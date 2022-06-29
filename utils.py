import pandas as pd
from os.path import exists


def save_df(df, file_name, file_format):
    if file_format == "csv":
        df.to_csv(file_name + ".csv", index=False, index_label=False)
    elif file_format == "json":
        df.to_json(file_name + ".json", index=False)
    elif file_format == "parquet":
        df.to_parquet(file_name + ".parquet")
    else:
        raise ValueError(file_format, "is not a correct format")


def open_df(file_name, file_format):
    file = file_name + "." + file_format
    if not exists(file):
        return pd.DataFrame(
            columns=[
                "country", "place_name", "place_id", "location", "station_name", "station_id", "station_stream_url"
            ]
        )
    if file_format == "csv":
        return pd.read_csv(file)
    if file_format == "json":
        return pd.read_json(file)
    if file_format == "parquet":
        return pd.read_parquet(file)
    raise ValueError(file_format, "is not a correct format")
