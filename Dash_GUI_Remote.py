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
import logging
import threading
import time
import paramiko as pa
import tqdm

#build the server for transffering to raspberry pi 
HOST= "10.0.0.96" #Standart loopback interface address(local host)
PORT=65432 # port to listen on ( non-privileged port are > 1023)
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
#variable to get the name of the file 
file_name=""
#if we want to create a temporary server 
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr =s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)
def thread_server():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr =s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data=conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


# server_thread=threading.Thread(target=thread_server)
# server_thread.start()
app=Dash(__name__)

dir_path=os.getcwd()
init_file_path=dir_path
# files_in_dir=os.listdir('/remote_gui_project/')
# for file_dir in files_in_dir:
#     print(file_dir)




app.layout = html.Div([
        html.H1('Raspberry Data Transfer protocol',style={'textAlign':'center', 'color':'Blue'}),
        html.Br(),
        'Select file to upload to your send list',
        
        # dcc.Input(id='Raspberry_ip',type='text',value='0.0.0.0'),
        # dcc.Input(id='Raspberry_port',type='text',value='00000'),
        
         
        
        dcc.Upload(
            id='upload_file',
            children=html.Div(['Drag and Drop or',html.A('Select Files')]),
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
            html.Br(),
            dcc.Dropdown(id='dynamic_file_dropdown'),
            # html.Div(id='files_list'),
            dcc.Input(id='file_to_sent',type='text',value='No files were chosen'),
            html.Br(),
            html.Button(id='send_button',n_clicks=0,children='Send'),
            dcc.Input(id='acknowledge_from_pi',type='text',value='No Ack recieve')
    ],
    style={'background':'LightGreen','height':"100vh",'width':"100vw"}
)



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
def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(dir_path, name), "wb") as fp:
        fp.write(base64.decodebytes(data))
        
        
        

# @app.callback(
#     Output("files_list", "children"),
#     [Input("upload_file", "filename"), Input("upload_file", "contents")],
#     #prevent_initial_call=True
# )
# def update_output(uploaded_filenames, uploaded_file_contents):
#     """Save uploaded files and regenerate the file list."""
#     global files
#     if uploaded_filenames is not None and uploaded_file_contents is not None:
#         for name, data in zip(uploaded_filenames, uploaded_file_contents):
#             save_file(name, data)

#     files = uploaded_files()
#     if len(files) == 0:
#         return [html.Li("No files yet!")]
#     else:
#         return [html.Li(file_download_link(filename)) for filename in files]
    
    
@app.callback(Output("dynamic_file_dropdown", "options"),
    [Input("upload_file", "filename"), Input("upload_file", "contents")],
    
)
def update_options(uploaded_filenames, uploaded_file_contents):
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        # return [html.Li(file_download_link(filename)) for filename in files]
        return files


@app.callback(Output("file_to_sent","value"),
              Input('dynamic_file_dropdown','value'),prevent_initial_call=True
              )
def update_sent_file(value):
    file_name=value
    print(f"you decided to send {file_name}")
    return value

@app.callback(Output("acknowledge_from_pi","value"),
              [Input('dynamic_file_dropdown','value')],prevent_initial_call=True
              )
def host_server_function(value_of_file):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr =s.accept()
        with conn:
            print(f"Connected by {addr}")
            print(f"sending {value_of_file} to raspberry pi")
            # filesize=os.path.getsize(file_name)
            while True:
                conn.sendall(str.encode(value_of_file))
                data=conn.recv(1024)
                if not data:
                    break
                print(f"the data we got is {data} ")
                return "data send"
            # s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.bind((HOST, PORT))
            # s.listen()
            # conn, addr =s.accept()
            # progress = tqdm.tqdm(range(filesize), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
            # with open(file_name,"rb") as f:
            #     while True:
            #         #read bytes from file 
            #         bytes_read=f.read(BUFFER_SIZE)
            #         if not bytes_read:
            #             #file transmitting is done 
            #             break
            #         #we used sendall to assure transmittion in busy network
                    

        


    



if __name__ == '__main__':
    app.run_server(debug=True)