import dash
import dash_bootstrap_components as dbc

dash_app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.SANDSTONE,
        "https://redmediadwh.z6.web.core.windows.net/assets/PublicisTemplate.css",
        # "assets/css/PublicisTemplate.css"
    ],
    external_scripts=[
        {"src": "https://kit.fontawesome.com/909a5e3baa.js", "crossorigin": "anonymous"}
    ],
)
