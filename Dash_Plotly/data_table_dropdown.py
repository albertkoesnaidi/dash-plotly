import pandas as pd
import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv('../Data/co2_data.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


countries = ['Indonesia', 'Japan', 'United States', 'Thailand', 'Vietnam', 'Canada', 'Myanmar', 'Norway', 'Germany', 'France']
dd_cols = ['coal_co2', 'cumulative_co2', 'cement_co2', 'cumulative_cement_co2', 'total_ghg']
df_table = df[(df['year'] == 2021) & df['country'].isin(countries)][['country', 'population', 'co2', 'co2_per_capita' ,'energy_per_capita','primary_energy_consumption']]


app.layout = html.Div([
        html.Div([ #tabledata
            dash_table.DataTable(
                id = 'datatable_id',
                data = df_table.to_dict('records'),
                columns = [{'name':i, 'id':i, 'deletable':False, 'selectable':False} for i in df_table.columns],
                editable=False,
                #filter_action='native',
                row_selectable='multi',
                selected_rows=[],
                #sort_action='native',
                # page_action='native',
                # page_current=0,
                # page_size=10,
                page_action='none',
                style_cell={
                        'whiteSpace': 'normal'
                            },
                fixed_rows={ 'headers': True, 'data': 0 },
                virtualization=False,
            )
        ]),
        html.Div([ #dropdowns main
            html.Div([ #dropdown1
                dcc.Dropdown(
                        id='line_dd',
                        options=[
                            {'label':i, 'value':i} for i in df.columns[df.columns.isin(dd_cols)]
                        ],
                        value='coal_co2',
                        multi=False,
                        clearable=False,
                        style={'margin-top':'10px'}
                )
            ], className='six columns'),
            html.Div([ #dropdown2
                dcc.Dropdown(
                        id='line2_dd',
                        options=[
                            {'label':i, 'value':i} for i in df.columns[df.columns.isin(dd_cols)]
                        ],
                        value='coal_co2',
                        multi=False,
                        clearable=False,
                        style={'margin-top':'10px'}
                )
            ],className='six columns')
        ], className='row'),
        html.Div([ #Graphs
            html.Div([
                dcc.Graph(id='line_graph')
            ], className='six columns'),
            html.Div([
                dcc.Graph(id='line2_graph')
            ], className='six columns')
        ], className='row')
])

@app.callback(
    Output(component_id='line_graph', component_property='figure'),
    Output(component_id='line2_graph', component_property='figure'),
    Input(component_id='datatable_id', component_property='selected_rows'),
    Input(component_id='datatable_id', component_property='data'), # data to access the data table (country, population, etc)
    Input(component_id='line_dd', component_property='value'),
    Input(component_id='line2_dd', component_property='value')
)
def update_graphs(sel_rows,d ,val1,val2):
    df1 = df.copy(deep=True)
    fig = go.Figure()
    fig2 = go.Figure()
    if len(sel_rows)==0 :
        fig.add_trace(go.Scatter(x=df1[df1['country']=='Indonesia']['year'], y=df1[df1['country']=='Indonesia'][val1], name='Indonesia' ,mode='lines' ))
        fig2.add_trace(go.Scatter(x=df1[df1['country']=='Indonesia']['year'], y=df1[df1['country']=='Indonesia'][val2], name='Indonesia' ,mode='lines'))
    elif len(sel_rows)>=1:
        for i in sel_rows:
            fig.add_trace(go.Scatter(x=df1[df1['country']==d[i]['country']]['year'], y=df1[df1['country']==d[i]['country']][val1] , mode='lines', name=d[i]['country']))
            fig2.add_trace(go.Scatter(x=df1[df1['country']==d[i]['country']]['year'], y=df1[df1['country']==d[i]['country']][val2] , mode='lines', name=d[i]['country']))
    return fig, fig2


if __name__ == '__main__':
    app.run_server(debug=True)