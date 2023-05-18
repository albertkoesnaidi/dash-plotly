import pandas as pd
import numpy as np

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv('../Data/games_sales.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Markdown(children='', id='text_header', style={'fontSize':24}),
        dcc.Dropdown(
                    id='year_dropdown',
                    options=[
                        {'label':'2010', 'value':2010},
                        {'label':'2011', 'value':2011},
                        {'label':'2012', 'value':2012},
                        {'label':'2013', 'value':2013},
                        {'label':'2014', 'value':2014},
                        {'label':'2015', 'value':2015},
                        {'label':'2016', 'value':2016},
                        {'label':'2017', 'value':2017},
                    ],
                    value=2010,
                    multi=False,
                    clearable=False,
                    style={'width':'30%'}
        ),
        dcc.Dropdown(
                    id='pie_dropdown',
                    options=[
                        {'label':'Platform', 'value':'Platform'},
                        {'label':'Genre', 'value':'Genre'},
                        {'label':'Publisher', 'value':'Publisher'},
                    ],
                    value='Genre', #yg ditampilkan pertama
                    multi=False, #only one value. if multiple values from the user than True
                    clearable=False, #we dont want the dropdown has no value
                    style={'width':'30%'}
        ),       
    ]),
    html.Div([
        dcc.Graph(id='pie_graph')
    ]),
])

# @app.callback(
#         Output(component_id='text_header', component_property='children'),
#         Input(component_id='year_dropdown', component_property='value')
# )
# def update_text(callback_year):
#     return f'the year is {callback_year}'


#################################################################
@app.callback(
    Output(component_id='text_header', component_property='children'),
    Output(component_id='pie_graph', component_property='figure'),
    Input(component_id='year_dropdown', component_property='value'),
    Input(component_id='pie_dropdown', component_property='value')
)
def update_graph(callback_year, callback_pie):
    #pie_df = df.copy(deep=True) #it is necessary to create a deep copy of the dataframe (must!)
    pie_df = df[df['Year']==callback_year][['Platform', 'Genre', 'Publisher']]
    
    pie = px.pie(data_frame=pie_df, names=callback_pie, hole=0.3)
    return f'the year is {callback_year}', pie
    




if __name__ == '__main__':
    app.run_server(debug=True)