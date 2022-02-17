# Data-Viz-Start-Up

Please Import and install these librairies and links

from plotly.subplots import make_subplots
import numpy as np
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly
import random
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
