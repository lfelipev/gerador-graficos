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

from django_plotly_dash import DjangoDash

# Read plotly example dataframe to plot barchart
import plotly.express as px
df = px.data.gapminder().query("country=='India'")

external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css']

# Important: Define Id for Plotly Dash integration in Django
app = DjangoDash('dash_integration_id')

##
df_dim = pd.read_csv('django_dash/dimensao_est.csv', sep=';') 

df_dim = df_dim.iloc[[2]]
df2 = pd.melt(df_dim, value_vars=['E_ESCV', 'E_PROFV', 'E_FAMV', 'E_COMV', 'E_ESTV'], var_name='dim', value_name='medias')

row = df2['dim'].tolist()
col = df2['medias'].tolist()
col = list(map(int, col))


fig = px.line_polar(df2, r='medias', theta='dim', line_close=True, markers=True, line_shape='linear', range_r=[1,7])

### Tabelas
fatores_melhores = pd.read_csv('django_dash/melhores.csv', sep=',')

fatores_piores = pd.read_csv('django_dash/piores.csv', sep=',')

fatores_medios = pd.read_csv('django_dash/medios.csv', sep=',')
## End Tabelas

## Geomap
with urlopen('https://raw.githubusercontent.com/CaioAbdon/georeferenciaTED/main/municipios_brasil.json') as response:
    counties = json.load(response)

# Municipios
municipio = pd.read_csv('django_dash/municipio.csv', sep=',')

fig_municipio = px.choropleth(municipio, geojson=counties, locations='codmunicipio', color='percentual',
                           color_continuous_scale="Blues",
                           #range_color=(0, 12),
                           featureidkey="properties.id",
                           scope="south america",
                           #labels={'unemp':'unemployment rate'}
                          )
fig_municipio.update_geos(fitbounds="locations", visible=True)
fig_municipio.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Estado
with urlopen('https://raw.githubusercontent.com/CaioAbdon/georeferenciaTED/main/ufBrasil2.json') as response:
    counties = json.load(response)

estado = pd.read_csv('django_dash/estado.csv', sep=',')

fig_estado = px.choropleth(estado, geojson=counties, locations='geocodigo', color='percentual',
                           color_continuous_scale="Blues",
                           #range_color=(0, 12),
                           featureidkey="properties.GEOCODIGO",
                           scope="south america",
                           #labels={'unemp':'unemployment rate'}
                          )
#ALTERAR O PARAMETRO VISIBLE PARA FALSE CASO SÓ SE QUEIRA MOSTRAR A PLOTAGEM DO PARÁ
fig_estado.update_geos(fitbounds="locations", visible=False)
fig_estado.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Regiao
with urlopen('https://raw.githubusercontent.com/CaioAbdon/georeferenciaTED/main/RegioesBrasil.json') as response:
    counties = json.load(response)
regiao = pd.read_csv('django_dash/regiao.csv', sep=',')

fig_regiao = px.choropleth(regiao, geojson=counties, locations='cod_regiao', color='percentual',
                           color_continuous_scale="Blues",
                           #range_color=(0, 12),
                           featureidkey="properties.ID",
                           scope="south america",
                           #labels={'unemp':'unemployment rate'}
                          )
#ALTERAR O PARAMETRO VISIBLE PARA FALSE CASO SÓ SE QUEIRA MOSTRAR A PLOTAGEM DO PARÁ
fig_regiao.update_geos(fitbounds="locations", visible=False)
fig_regiao.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

### End Geomap

app.css.append_css({
"external_url": external_stylesheets
})
app.layout = html.Div(
    html.Div([
        # Adding one extar Div
        html.Div([
            html.H1(children='Multiple Application'),
            html.H3(children='Line chart over time'),
            html.Div(children='Dash: Python framework to build web application'),
        ], className = 'row'),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='bar-chart',
                    figure={
                        'data': [
                            {'x': df['year'], 'y': df['pop'], 'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': 'Bar Chart Visualization'
                        }
                    }
                ),
            ], className = 'six columns'),

            # Adding one more app/component
            html.Div([
                dcc.Graph(
                    id='line-chart',
                    figure={
                        'data': [
                            {'x': df['year'], 'y': df['pop'], 'type': 'line', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': 'Line Chart Visualization'
                        }
                    }
                )
            ], className = 'six columns'),

            html.Div([
                dcc.Graph(
                    figure=fig
                )
            ]),

            html.Div([
                dcc.Graph(
                    figure=fig_municipio
                )
            ]),

            html.Div([
                dcc.Graph(
                    figure=fig_estado
                )
            ]),

            html.Div([
                dcc.Graph(
                    figure=fig_regiao
                )
            ]),

            ## Melhores alunos
            html.Div([
                dash_table.DataTable(
                    data=fatores_melhores.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in fatores_melhores.columns],
                    page_size=10,
                    style_header={
                            'background': 'white',
                            'fontWeight': 'bold'
                        },
                    style_data={
                        'backgroundColor': 'rgb(179,212,139)'
                    }
                )
            ]),

            # Piores alunos
            html.Div([
                dash_table.DataTable(
                    data=fatores_piores.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in fatores_piores.columns],
                    page_size=10,
                    style_header={
                            'background': 'white',
                            'fontWeight': 'bold'
                        },
                    style_data={
                        'backgroundColor': 'rgb(246,182,181)'
                    }
                )
            ]),

            # Alunos Medianos
            html.Div([
                dash_table.DataTable(
                    data=fatores_medios.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in fatores_medios.columns],
                    page_size=10,
                    style_header={
                            'background': 'white',
                            'fontWeight': 'bold'
                        },
                    style_data={
                        'backgroundColor': 'rgb(250,227,147)'
                    }
                )
            ]),

            html.Div([
                daq.Gauge(
                    color={"gradient":False,"ranges":{"green":[0,2.44],"yellow":[2.44,3.42],"red":[3.42,7]}},
                    value=2,
                    label='Estudante-Estudante',
                    max=7,
                    min=0,
                    showCurrentValue=True
                )
            ])

        ], className = 'row')
    ])
)

@app.callback(
    dash.dependencies.Output('line_polar', 'figure'),
    [dash.dependencies.Input('', '')])
def update_graph(Country):
    trace = px.line_polar(df2, theta='dim', r='medias', line_close=True, template="plotly_dark",
                          title='Summary of Factors (%)')
    return trace

if __name__ == '__main__':
    app.run_server(8052, debug=False)