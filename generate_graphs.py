from typing import Dict, Any
import pandas as pd
import numpy as np
import plotly

import plotly.express as px

if __name__ == "__main__":
    pass

pd.options.mode.chained_assignment = None  # default='warn'


def generate_scattermap(frame: pd.DataFrame, size_var,
                        color_var) -> plotly.graph_objs.Figure:
    exact_rows = frame[frame["exact"] == True]
    exact_rows.dropna(subset=size_var, inplace=True)
    exact_rows.dropna(subset=color_var, inplace=True)
    fig_mapscat = px.scatter_mapbox(exact_rows, lat="lat", lon="long",
                            color=color_var, size=size_var)
    # , color_continuous_scale="aggrnyl_r")
    # fig_mapscat.update_traces(cluster=dict(enabled=True, color="red", opacity=0.7, maxzoom=11))
    fig_mapscat.update_layout({
        "margin": dict(l=20, r=20, t=20, b=20),
        "showlegend": True,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "white"},
        "mapbox_style": "dark"})
    return fig_mapscat


def generate_choropleth(frame: pd.DataFrame, poly_data) -> plotly.graph_objs.Figure:
    fig = px.choropleth_mapbox(frame, geojson=poly_data, locations=frame.index,
                               featureidkey="properties.neighborhood",
                               color="mean", center={"lat": 40.7128, "lon": -74.0060}, zoom=10,
                               color_continuous_scale="aggrnyl_r")
    fig.update_geos(fitbounds="locations")
    fig.update_layout({
        "margin": dict(l=20, r=20, t=20, b=20),
        "showlegend": True,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "white"},
        "mapbox_style": "dark"})
    return fig


def generate_scatter(frame, xval, yval, color="host_identity_verified"):
    frame = frame.dropna(subset=(yval)).dropna(subset=xval)
    if xval == "price":
        frame["price"] = frame["price"].apply(lambda x: float(x))
    fig = px.scatter(frame, x=xval, y=yval, color=color, opacity=0.7)
    fig.update_layout({
        "margin": dict(l=20, r=20, t=20, b=20),
        "showlegend": True,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "white"}})
    return fig
