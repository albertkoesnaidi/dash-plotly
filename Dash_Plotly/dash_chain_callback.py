import dash
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
                dcc.Dropdown(
                        id='dropdown_1',
                        options= ['Surabaya', 'Jakarta', 'Sidoarjo'],
                        value='Surabaya',
                        clearable=False,
                        multi=False,
                        style={'width':'40%'}
                ),
                dcc.RadioItems(options=['Sby1', 'Sby2', 'Sby3'], id='radio_1')
])

@app.callback(
    Output(component_id='radio_1', component_property='options'),
    Input(component_id='dropdown_1', component_property='value')
)

def update_radio(callback_dropdown):
    if callback_dropdown == 'Surabaya':
        return ['Sby1', 'Sby2', 'Sby3']
    elif callback_dropdown == 'Jakarta':
        return ['Jkt1', 'Jkt2', 'Jkt3']
    elif callback_dropdown == 'Sidoarjo':
        return ['Sid1', 'Sid2', 'Sid3']
    else:
        return []


if __name__ == '__main__':
    app.run_server(debug=True)