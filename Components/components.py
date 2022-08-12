import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
import plotly.graph_objects as go
import plotly.io as pio


select_jobnumber = dcc.Dropdown(
    id="select-jobnumber",
    options=[
    ],
    className="mb-2"
)

select_product = dcc.Dropdown(
    id = 'select_product',
    options=[
        {'label': 'Brandon', 'value': 'B'},
        {'label': 'Startrack', 'value': 'S'}
    ],
    placeholder="Vyber produkt",
    optionHeight=40
)

upload_component = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Hoď sem tu prcárnu nebo ',
            html.A('vyber soubor')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    )
])

jk1_pic = html.Img(id='jk1', src='/assets/jk1.png', className='center', alt ='Tady má být obrázek Jirky Káry. Jestli se nezobrazuje, je něco špatně.', height = 200, width =200)


alert_select_product = dbc.Alert("Ty vokurko! Vyber nejdřív, který produkt budeme zpracovávat!", color="danger")
alert_wrong_selection = dbc.Alert("Soubor musí být ve formátu .xlsx! Hlavně, že máš pivo, vole!", color="danger")
alert_select_file = dbc.Alert("Ty magore! Vyber nejdřív soubor, který budeme zpracovávat!", color="danger")
alert_failed_tests = dbc.Alert("Ajéje. Tenhle soubor přece nemůžeme uložit do databáze, není správně. Oprav to a zkus to znova.", color="danger")
alert_success_upload = dbc.Alert("Vynikající práce, o prcárnu na světě méně!", color="success")

#button_submit = html.Div(dbc.Button("Jdeme na to", color="primary"), className=".button-primary")
#button_submit = html.Div(dbc.Button("Jdeme na to", color="primary"), className=".button-primary")
button_submit = html.Button(
    children="Jdeme na to",
    id="button_1",
    type="submit",
    className="button-primary"
)

button_send = html.Button(
    children="Nahrát do databáze",
    id="button_2",
    type="submit",
    className="button-primary"
)

jobInput = dcc.Input(id="jobInput", type="text", placeholder="Job Number")
