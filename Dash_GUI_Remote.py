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
from dash.dependencies import Input, Output
import socket

#build the server for transffering to raspberry pi 
HOST= "10.0.0.96" #Standart loopback interface address(local host)
PORT=65432 # port to listen on ( non-privileged port are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr =s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


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
    for filename in os.listdir(dir_path):
        path = os.path.join(dir_path, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

@app.callback(
    Output("files_list", "children"),
    [Input("upload_file", "filename"), Input("upload_file", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    # if uploaded_filenames is not None and uploaded_file_contents is not None:
    #     for name, data in zip(uploaded_filenames, uploaded_file_contents):
    #         save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

if __name__ == '__main__':
    app.run_server(debug=True)