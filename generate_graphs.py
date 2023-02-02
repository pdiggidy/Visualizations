from typing import Dict, Any
import pandas as pd
import numpy as np
import plotly

import plotly.express as px

if __name__ == "__main__":
    pass

pd.options.mode.chained_assignment = None  # default='warn'


def generate_scattermap(frame: pd.DataFrame, size_var,
                        color_var, swatch, scale) -> plotly.graph_objs.Figure:
    exact_rows = frame[frame["exact"] == True]
    exact_rows.dropna(subset=size_var, inplace=True)
    exact_rows.dropna(subset=color_var, inplace=True)
    fig_mapscat = px.scatter_mapbox(exact_rows, lat="lat", lon="long",
                                    color=color_var, size=size_var, color_continuous_scale=swatch)
    # TODO Add scale
    fig_mapscat.update_layout({
        "margin": dict(l=20, r=20, t=20, b=20),
        "showlegend": True,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "white"},
        "mapbox_style": "dark"})
    return fig_mapscat


def generate_choropleth(frame: pd.DataFrame, poly_data, color_var, swatch) -> plotly.graph_objs.Figure:
    means = frame.groupby("neighbourhood").mean(numeric_only=True)
    fig = px.choropleth_mapbox(means, geojson=poly_data, locations=means.index,
                               featureidkey="properties.neighborhood",
                               color=color_var, center={"lat": 40.7128, "lon": -74.0060}, color_continuous_scale=swatch)  # , zoom=10)
    fig.update_geos(fitbounds="geojson")
    fig.update_layout({
        "margin": dict(l=20, r=20, t=20, b=20),
        "showlegend": True,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "white"},
        "mapbox_style": "dark"})
    return fig


def generate_scatter(frame, xval, yval, color="Host_Identity_Verified"):
    frame = frame.dropna(subset=(yval)).dropna(subset=xval)
    if xval == "Price":
        frame["Price"] = frame["Price"].apply(lambda x: float(x))
    fig = px.scatter(frame, x=xval, y=yval, color=color, opacity=0.7)
    fig.update_layout({
        "margin": dict(l=20, r=20, t=20, b=20),
        "showlegend": True,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "white"}})
    return fig


def generate_hist(frame, x_val, bins):
    fig = px.histogram(frame, x=x_val, color="Host_Identity_Verified", nbins=bins)
    fig.update_layout({
        "margin": dict(l=20, r=20, t=20, b=20),
        "showlegend": True,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "white"}})
    return fig
