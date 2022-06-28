import pandas as pd


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
    if file_format == "csv":
        return pd.read_csv(file_name + ".csv")
    if file_format == "json":
        return pd.read_json(file_name + ".json")
    if file_format == "parquet":
        return pd.read_parquet(file_name + ".parquet")
    raise ValueError(file_format, "is not a correct format")
