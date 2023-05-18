import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output
from dash import dcc, html

df = pd.read_csv('../Data/co2_data.csv')
cc = pd.read_csv('../Data/country_code_isoalpha.csv')
cc = cc[['name', 'alpha-3']]

df = df.merge(cc, left_on='country', right_on='name', how='right')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
            dcc.Graph(id='world_graph')
    ]),
    html.Div([
            dcc.Slider(min=1900, max=2021, step=2, id='my_slider', value = 1900,dots=False, marks={i: '{}'.format(i) for i in range(1900,2021,2)})
    ])
])

@app.callback(
    Output(component_id='world_graph', component_property='figure'),
    Input(component_id='my_slider', component_property='value')
)

def update_graph(val):
    df1 = df.copy(deep=True)
    df1 = df1[df1['year']==val]

    fig = px.choropleth(data_frame=df1, locations='alpha-3', color='co2_per_capita', hover_name='country', projection='natural earth',color_continuous_scale=px.colors.sequential.Plasma, range_color=[0,100])
    fig.update_layout(margin=dict(l=2, r=2, t=1, b=1))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)