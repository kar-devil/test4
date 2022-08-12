import dash_bootstrap_components as dbc
from dash import html
from _dash_app import dash_app
from Components.components import *


layout = html.Div(
    children=[
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    html.Img(
                        src=dash_app.get_asset_url("images/pub_logo.png"),
                        id='publicis-logo',
                    ),
                    class_name="col-auto me-auto"
                ),
                dbc.Col(
                    [
                        html.A(
                            "O appce",
                            id="app-info-p",
                        ),
                    ],class_name="col-auto"
                )
            ], class_name="row gx-0"
        ),
        dbc.Offcanvas(
            html.P(
                "This is the content of the Offcanvas. "
            ),
            id="offcanvas",
            title="Data Products App",
            is_open=False,
        ),
        html.Br(), # tady se láme chleba :D
        dbc.Container([ # obrázek
                    html.Br(),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(), width=4),
                        dbc.Col(html.Div(jk1_pic), width=4),
                        dbc.Col(html.Div(), width=4)
                        ],className="g-0", align="center", justify="center"),
                    html.Br()
        ]),
        dbc.Container([ # welcome
                    dbc.Row([
                        dbc.Col(html.Div(), width=1),
                        dbc.Col(html.Div(className="main", children=[
                            html.H1("Vítej v království analytických produktů!")]), width=10),
                        dbc.Col(html.Div(), width=1)]
                    ),
                    dbc.Row(dbc.Col(html.Div(className="main roller", children=[
                        html.Span(id='rolltext', children=[
                            html.H1('No', className='roller'),
                            html.H1('Tak', className='roller'),
                            html.H1('Děléééj', className='roller'),
                            html.Span(id='spare-time', children=[html.H2('Už jsi to měl mít 4 minuty')])
                                 ])]),
                                    width=12)),
                    html.Div("", className='small_spacing'),
        ]),
        dbc.Container([ # upload component
                     dbc.Row([
                        dbc.Col(html.Div(), width=2),
                        dbc.Col(html.Div(upload_component), width=8),
                        dbc.Col(html.Div(), width=2)
                    ], className="g-0", align="center", justify="center"),
                    dbc.Row([
                        dbc.Col(html.Div(), width=4),
                        dbc.Col(html.Div(select_product), width=2),
                        dbc.Col(html.Div(), width=1),
                        dbc.Col(html.Div(button_submit), width=2),
                        dbc.Col(html.Div(), width=3)
                    ], className="g-0", align="center", justify="center"),
                    html.Div("", className='small_spacing'),
                    dbc.Row(
                        dbc.Col(html.Div(), width=12)),
                    html.Div(id='output-div'),
                    html.Div(id='output-datatable')
                ]
                )
    ]
)
