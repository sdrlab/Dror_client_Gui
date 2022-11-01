# Run this app with `Dash_GUI_Remote` and
# visit http://127.0.0.1:8050/ in your web browser.
import base64
import datetime
import io
import fnmatch
import glob
import os
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from urllib.parse import quote as urlquote

app=Dash(__name__)

dir_path=os.getcwd()

# files_in_dir=os.listdir('/remote_gui_project/')
# for file_dir in files_in_dir:
#     print(file_dir)

app.layout = html.Div([
    html.H1('Raspberry Data Transfer protocol',style={'textAlign':'center', 'color':'Blue'}),
    html.Br(),
    'Select file to upload to your raspberry pi',
    
    
    dcc.Upload(id='upload_file',children=html.Div(['Drag and Drop or',html.A('Select Files')]),
            style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'background':'DeepSkyBlue'
            },
            # Allow multiple files to be uploaded
            multiple=True
            ),
            html.H3(['the selected folder is :' ,dir_path]),
            'the files in the folders are',
            html.Div(id='files_list'),
],style={'background':'LightGreen','height':"100vh",'width':"100vw"})

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "dir_path{}".format(urlquote(filename))
    return html.A(filename, href=location)

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files
if __name__ == '__main__':
    app.run_server(debug=True)