from typing import Dict, Any
import pandas as pd
import numpy as np

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

df_clean = is_exact(df_clean)
