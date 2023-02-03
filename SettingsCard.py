import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import Dash, dcc, html, Input, Output

# ['id', 'NAME', 'host id', 'host_identity_verified', 'host name',
#        'neighbourhood group', 'neighbourhood', 'lat', 'long', 'country',
#        'country code', 'instant_bookable', 'cancellation_policy', 'room type',
#        'Construction year', 'price', 'service fee', 'minimum nights',
#        'number of reviews', 'last review', 'reviews per month',
#        'review rate number', 'calculated host listings count',
#        'availability 365', 'house_rules', 'license', 'exact',
#        'distanceTimeSquare']
hist_color_options = ["None", "Price", "Minimum Nights", "Number of Reviews", "Reviews Per Month", "Review Score",
                      "Availability 365", "Host_Identity_Verified"]
items = ["Price", "Minimum Nights", "Number of Reviews", "Reviews Per Month", "Review Score", "Availability 365"]
items_color = ["aggrnyl_r", "agsunset", "blackbody", "bluered", "blues", "blugrn", "bluyl", "brwnyl",
               "bugn", "bupu", "burg", "burgyl", "cividis", "darkmint", "electric", "emrld",
               "gnbu", "greens", "greys", "hot", "inferno", "jet", "magenta", "magma",
               "mint", "orrd", "oranges", "oryel", "peach", "pinkyl", "plasma", "plotly3",
               "pubu", "pubugn", "purd", "purp", "purples", "purpor", "rainbow", "rdbu",
               "rdpu", "redor", "reds", "sunset", "sunsetdark", "teal", "tealgrn", "turbo",
               "viridis", "ylgn", "ylgnbu", "ylorbr", "ylorrd", "algae", "amp", "deep",
               "dense", "gray", "haline", "ice", "matter", "solar", "speed", "tempo",
               "thermal", "turbid", "armyrose", "brbg", "earth", "fall", "geyser", "prgn",
               "piyg", "picnic", "portland", "puor", "rdgy", "rdylbu", "rdylgn", "spectral",
               "tealrose", "temps", "tropic", "balance", "curl", "delta", "oxy", "edge",
               "hsv", "icefire", "phase", "twilight", "mrybm", "mygbm"]

card_layout = dbc.Card([
    dbc.CardBody([
        html.H4("Settings"),
        dbc.Row([
            dbc.Col(
                html.H6("Color Swatch"), width="auto"),
            dbc.Col(dcc.Dropdown(options=items_color, value="aggrnyl_r", id="swatch"), width="6")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(
                html.H6("Map Color Variable"), width="auto"),
            dbc.Col(dcc.Dropdown(options=items, value="Price", id="map_Color"), width="6")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H6("Map Size Variable"), width="auto"),
            dbc.Col(dcc.Dropdown(options=items, value="Review Score", id="map_Size"), width="6")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H6("Map Size Scale"), width="auto"),
            dbc.Col(dcc.Input(value="1", id="map_Scale"), width="6")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H6("Neighbourhood Color"), width="auto"),
            dbc.Col(dcc.Dropdown(options=items, value="Review Score", id="chloro_Color"), width="6")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H6("Histogram Variable"), width="auto"),
            dbc.Col(dcc.Dropdown(options=items, value="Price", id="hist_Var"), width="6")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H6("Histogram Bins"), width="auto"),
            dbc.Col(dcc.Input(value="200", id="hist_Bins"), width="6")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H6("Histogram Color"), width="auto"),
            dbc.Col(dcc.Dropdown(options=hist_color_options, value="Host_Identity_Verified", id="hist_Color"),
                    width="6")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H6("Slider Variable"), width="auto"),
            dbc.Col(dcc.Dropdown(options=items, value="Price", id="slider_Var"), width="6")
        ], align="center", justify="between")
    ])
])

# TODO Validate Input box
# TODO Edit onhover of graphs
