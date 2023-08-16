from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('../Data/owid-energy-data.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
        dcc.Dropdown(options=[
                {'label':'Indonesia', 'value':'Indonesia'},
                {'label':'Japan', 'value':'Japan'},
                {'label':'Philippines', 'value':'Philippines'},
                {'label':'Thailand', 'value':'Thailand'},
                {'label':'Singapore', 'value':'Singapore'},
                {'label':'Malaysia', 'value':'Malaysia'}
        ], value='Indonesia', id='dd1'),
        html.Div([
            dcc.Markdown(id='text1', children=''),
            dcc.Graph(id='line_graph')
        ]),
        html.Div([
            dcc.Graph(id='line_graph2')
        ]),
        html.Div([
            dcc.Graph(id = 'pie_fossil', className='six columns'),
            dcc.Graph(id = 'pie_renewables', className='six columns')
        ], className='row')
])

@app.callback(
        Output(component_id='text1', component_property='children'),
        Input(component_id='dd1', component_property='value'),
)
def update_text(value):
    return f'Country: {value}'

@app.callback(
    Output(component_id='line_graph', component_property='figure'),
    Input(component_id='dd1', component_property='value')
)
def update_graph(value):
    df1 = df[df['country']==value]
    df1 = df1.dropna(subset=['coal_electricity'])
    fig1 = px.line(data_frame=df1, x='year', y='coal_electricity')
    return fig1

@app.callback(
    Output(component_id='line_graph2', component_property='figure'),
    Input(component_id='dd1', component_property='value')
)
def update_graph2(value):
    df2 = df[df['country']==value]
    df2 = df2.dropna(subset=['coal_electricity'])
    df2['fossil'] = df2['coal_electricity'] + df2['oil_electricity'] + df2['gas_electricity']
    df2['renewables'] = df2['renewables_electricity'] + df2['other_renewable_electricity']
    fig2= go.Figure()
    fig2.add_scatter(x=df2['year'], y=df2['fossil'], mode='lines', name='Fossil Fuels')
    fig2.add_scatter(x=df2['year'], y=df2['renewables'], mode='lines', name='Renewables Sources')
    fig2.update_layout(xaxis_title='Year' ,yaxis_title='Energy [MWh]')
    return fig2

@app.callback(
    Output(component_id='pie_fossil', component_property='figure'),
    Input(component_id='dd1', component_property='value'),
    Input(component_id='line_graph2', component_property='clickData')
)
def update_pie1(value, clickData):
    df2 = df[df['country']==value][['year','coal_electricity', 'oil_electricity', 'gas_electricity']]
    df2 = df2.dropna(subset=['coal_electricity']).set_index('year').T
    if not clickData:
        fig3 = px.pie(data_frame=df2, values=2000, names=df2.index)
    else:
        fig3 = px.pie(data_frame=df2, values=clickData['points'][0]['x'], names=df2.index)
    fig3.update_layout(title='Fossil Fuel Mix Diagramm')
    return fig3

@app.callback(
    Output(component_id='pie_renewables', component_property='figure'),
    Input(component_id='dd1', component_property='value'),
    Input(component_id='line_graph2', component_property='clickData')
)
def update_pie1(value, clickData):
    df3 = df[df['country']==value][['year','solar_electricity', 'hydro_electricity', 'biofuel_electricity', 'wind_electricity']]
    df3 = df3.dropna(subset=['solar_electricity']).set_index('year').T
    if not clickData:
        fig4 = px.pie(data_frame=df3, values=2000, names=df3.index)
    else:
        fig4 = px.pie(data_frame=df3, values=clickData['points'][0]['x'], names=df3.index)
    fig4.update_layout(title='Renewables Energy Mix Diagramm', showlegend=True)
    return fig4

if __name__ == '__main__':
    app.run(debug=True)