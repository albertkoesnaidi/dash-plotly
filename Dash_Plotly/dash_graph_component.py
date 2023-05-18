import dash
from dash import dcc, html
import plotly_express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv('../Data/co2_data.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
country = ['Indonesia', 'Germany', 'Singapore', 'Brazil', 'United States', 'Afghanistan', 'Thailand', 'Australia', 'Japan']

app.layout= html.Div([
    dcc.Dropdown(id='country_dropdown', 
                 value=['Indonesia', 'Germany'],
                 multi=True,
                 options=[{'label':i,'value':i} for i in country],
                 style= {'width':'60%'}
                 ),
    html.Div([
        dcc.Markdown(id='text_markdown1', children=''),
        dcc.Graph(id='line_graph', className='five columns'),
        dcc.Graph(id='bar_graph', className='five columns')
    ])
],className='row')

@app.callback(
    Output(component_id='line_graph', component_property='figure'),
    Input(component_id='country_dropdown', component_property='value')
)
def update_graph(countries):
    df1=df.copy(deep=True)
    fig = go.Figure()
    for i in countries:
        fig.add_trace(go.Scatter(x=df1[df1['country']==i]['year'], y=df1[df1['country']==i]['co2'], mode='lines', name=i, customdata=df1[df1['country']==i]['population'], hoverinfo='x'))
        fig.update_traces(
                hovertemplate="<br>".join([
                    "Year: %{x}",
                    "CO2: %{y}",
                    "Population: %{customdata}",
                ])
        )
    return fig


@app.callback(
    Output(component_id='text_markdown1', component_property='children'),
    Output(component_id='bar_graph', component_property='figure'),
    # Output(component_id='text_markdown1', component_property='children'),
    Input(component_id='country_dropdown', component_property='value'),
    Input(component_id='line_graph', component_property='hoverData')
    
)
def update_bar(countries, hoverdata):
    if hoverdata is None:
        df2 = df.copy(deep=True)
        df2 = df2[(df2['year']==2000) & df2['country'].isin(countries)]
        fig2 = px.pie(data_frame=df2, values='population', names='country')
        return f'The Year is 2000', fig2
    else:
        df2=df.copy(deep=True)
        hov_year = hoverdata['points'][0]['x']
        df2 = df2[(df2['year']==hov_year) & (df2['country'].isin(countries))]
        fig2 = px.pie(data_frame=df2, values='population', names='country')
        return f'The Year is {hov_year}', fig2


if __name__ == '__main__':
    app.run_server(debug=True)
