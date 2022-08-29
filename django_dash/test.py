import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from collections import OrderedDict
from dash import dash_table
from urllib.request import urlopen
import json
import plotly.express as px


with urlopen('https://raw.githubusercontent.com/CaioAbdon/georeferenciaTED/main/RegioesBrasil.json') as response:
    counties = json.load(response)

regiao = pd.read_csv('django_dash/regiao.csv', sep=',')

fig = px.choropleth(regiao, geojson=counties, locations='cod_regiao', color='percentual',
                           color_continuous_scale="Blues",
                           #range_color=(0, 12),
                           featureidkey="properties.ID",
                           scope="south america",
                           #labels={'unemp':'unemployment rate'}
                          )
#ALTERAR O PARAMETRO VISIBLE PARA FALSE CASO SÓ SE QUEIRA MOSTRAR A PLOTAGEM DO
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()