from typing import Dict, Any
import pandas as pd
import numpy as np
import plotly

import plotly.express as px

if __name__ == "__main__":
    pass

def generate_scatter(frame: pd.DataFrame, size_var="number of reviews", color_var="scaled") -> plotly.graph_objs.Figure:
    exact_rows = frame[frame["exact"] == True]
    fig = px.scatter_mapbox(exact_rows, lat="lat", lon="long",
                            color=color_var, size=size_var,
                            color_continuous_scale="aggrnyl_r")
    fig.update_traces(cluster=dict(enabled=True, color="red", opacity=0.7))
    return fig


def generate_choropleth(frame: pd.DataFrame, poly_data) -> plotly.graph_objs.Figure:
    fig = px.choropleth_mapbox(frame, geojson=poly_data, locations="neighbourhood",
                               featureidkey="properties.neighborhood",
                               color="scaled", center={"lat": 40.7128, "lon": -74.0060}, zoom=10,
                               color_continuous_scale="aggrnyl_r")
    fig.update_geos(fitbounds="locations", visible=False)
    return fig
