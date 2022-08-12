import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import time
from Components.components import alert_select_product, alert_wrong_selection, alert_select_file, button_send
from Components.layout import layout
from _dash_app import dash_app
#from Components.functions import TestFunction, createFinalExport
from datetime import datetime
# from redpackage.azure.blob import Blob

# ---------------- Initialize dash app server ----------------------------------------

#dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.title = "Datová prcárna"
dash_app.description = "Tato aplikace zpracovává data pro datové produkty"
app = dash_app.server
dash_app.layout = layout

if __name__ == '__main__':
    dash_app.run_server(debug=True)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@dash_app.callback(
    [
        Output("offcanvas", "is_open"),
        Output('offcanvas', 'children')
    ],
    Input("app-info-p", "n_clicks"),
    State("offcanvas", "is_open"),
)

def toggle_offcanvas(n1, is_open):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'app-info-p' in changed_id:
        with open("README.md", encoding="utf-8") as f:
            f_content = f.read()
        return not is_open, dcc.Markdown(f_content)

    return is_open, None

@dash_app.callback(Output('output-datatable', 'children'),
                   Input('upload-data', 'contents'),
                   Input('button_1', 'n_clicks'),
                   State('select_product', 'value'),
                   State('upload-data', 'filename'),
                   State('upload-data', 'last_modified')
                   )

def update_output(contents, n_clicks, value, filename, last_modified):
    if n_clicks == None:
        pass
    elif n_clicks >= 1:
        if contents == None:
            returnValue = alert_select_file
        elif contents is not None:
            if (value == 'S') or (value == 'B'):
                returnValue = TestFunction(contents, value, filename, last_modified)
            elif value == None:
                returnValue = alert_select_product
        return returnValue
    else:
        pass


@dash_app.callback(
    Output(component_id='my-output', component_property='children'),
    State(component_id='upload-data', component_property="contents"),
    State(component_id='select_product', component_property="value"),
    State("jobInput", "value"),
    Input('button_2', 'n_clicks')
)
def upload_to_dbo(contents,product, job, click):
    if click == None:
        pass
    elif click >= 1:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        return dt_string, product, job, createFinalExport()
