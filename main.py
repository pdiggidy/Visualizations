import jupyter_dash as dash
import pandas as pd
import numpy as np
from pandas._typing import DataFrame

df = pd.read_csv("tic_data.csv")
print(df.describe())


def count_nan(df: DataFrame) -> DataFrame:
    output = {}
    for i in df.columns:
        output[i] = df[i].isna().sum()
    return output


count_nan(df)
