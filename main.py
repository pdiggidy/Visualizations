from typing import Dict, Any

import jupyter_dash as dash
import pandas as pd
import numpy as np

df = pd.read_csv("Airbnb_Open_Data.csv", low_memory=False)
print(list(df.columns))

# for i in df.columns:  # Columns With NA values in them
#     count = df[i].isna().sum()
#     if count != 0:
#         print(f"Column: {i}, NAs: {count}")

df_clean = df
df_clean["host_identity_verified"] = df["host_identity_verified"].fillna("unconfirmed")  # If there's no information
# about verification assume it's not
df_clean["NAME"] = df["NAME"].fillna("unavailable")  # If there's no name replace it with "unavailable"
df_clean["host name"] = df["host name"].fillna("unavailable")  # If there's no host name replace it with unavailable

df_clean = df_clean.dropna(subset=["neighbourhood", "neighbourhood group", "long"], how="all")


# print("#####")
# for i in df_clean.columns:  # Columns With NA values in them
#     count = df_clean[i].isna().sum()
#     if count != 0:
#         print(f"Column: {i}, NAs: {count}")

def is_exact(data: pd.DataFrame) -> pd.DataFrame:
    data["exact"] = data["long"].notna()
    return data


df_clean = is_exact(df_clean)


