from typing import Dict, Any
import pandas as pd
import numpy as np
from POI import time_square

import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go


def is_exact(data: pd.DataFrame) -> pd.DataFrame:
    data["exact"] = data["long"].notna()
    return data


df = pd.read_csv("Airbnb_Open_Data.csv", low_memory=False)

df_clean = df
df_clean["host_identity_verified"] = df["host_identity_verified"].fillna("unconfirmed")  # If there's no information
# about verification assume it's not
df_clean["NAME"] = df["NAME"].fillna("unavailable")  # If there's no name replace it with "unavailable"
df_clean["host name"] = df["host name"].fillna("unavailable")  # If there's no host name replace it with unavailable

df_clean = df_clean.dropna(subset=["neighbourhood", "neighbourhood group", "long"], how="all")

df_clean["availability 365"] = df_clean["availability 365"].apply(lambda x: x if x <= 365 else np.nan)
df_clean["availability 365"] = df_clean["availability 365"].apply(lambda x: x if x >= 0 else np.nan)

df_clean = is_exact(df_clean)
df_clean["price"] = df_clean["price"].apply(lambda x: str(x).replace("$", "").replace(",", "")).astype(float)
df_clean["service fee"] = df_clean["service fee"].apply(lambda x: str(x).replace("$", "").replace(",", "")).astype(float)


df_clean["distanceTimeSquare"] = df_clean.apply(lambda x: time_square.calculate_distance(x.lat, x.long), axis=1)
df_clean.to_csv("AirbnbClean.csv")

means_list = []

means = df_clean.groupby("neighbourhood").describe()
cols = []
for col in df_clean.columns:
    try:
        mean = pd.DataFrame(means[col]["mean"])
        means_list.append(mean)
        cols.append(col)
    except KeyError as e:
        continue

df_means = pd.concat(means_list, axis=1)
df_means.columns = cols
df_means.drop(columns="id")
df_means.to_csv("neighb_means.csv")