# Run this app with `Dash_GUI_Remote` and
# visit http://127.0.0.1:8050/ in your web browser.

import os
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app=Dash(__name__)


app.layout = html.Div([
    html.H1('Raspberry Data Transfer protocol',style={'textAlign':'center', 'color':'Blue'}),
    html.Br(),
    'Select file to upload to your raspberry pi'
],style={'background':'LightGreen','height':"100vh",'width':"100vw"})




if __name__ == '__main__':
    app.run_server(debug=True)