# # Send a directmessage to another DS user
# {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}

# # Request unread message from the DS server
# {"token":"user_token", "directmessage": "new"}

# # Request all messages from the DS server
# {"token":"user_token", "directmessage": "all"}

# Simar Cheema
# simarc@uci.edu
# 31075859

import socket
import ds_protocol as dsp
from Profile import Profile
from pathlib import Path
import json

profile = Profile()
path = Path('.')

usr = 'dino321'
pwd = 'rose'
HOST = '168.235.86.101'
PORT = 3021
token = 'HhM7wvm7AaLNcKmcGAmVl5zTjK1WtJC9KSdrd/tZGlQ=' #dino321 token - got this by connecting to the server

def connect(server:str, port:int, usr:str, pwd:str):
  #Need Username and Password of User Trying to join the server in order to send or receive messages
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    join_msg = dsp.join(usr, pwd)
    client.settimeout(1)
    client.connect((server, port))
    _send = client.makefile('w')
    recv = client.makefile('r')
    _send.write(join_msg + '\r\n')
    _send.flush()
    srv_msg = recv.readline()
    try:
      x = dsp.extract_token(srv_msg)
      token = x.token
    except:
      token = None
    return token
    # print(srv_msg)
  
def send_message(server, port, token, msg, recipient):
  #Need Token of User Sending the Message and username of User receiving the message
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    msg = dsp.send_msg(token, msg, recipient)
    client.connect((server, port))
    _send = client.makefile('w')
    recv = client.makefile('r')
    _send.write(msg + '\r\n')
    _send.flush()
    srv_msg = recv.readline()
    print(srv_msg)
    print(srv_msg[23:28])
    return srv_msg

def request_all(server, port, token):
  #Need token of User trying to read all messages they have gotten
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    req = dsp.req_all(token)
    client.connect((server, port))
    _send = client.makefile('w')
    recv = client.makefile('r')
    _send.write(req + '\r\n')
    _send.flush()
    srv_msg = recv.readline()
    print(srv_msg)
    srv_msg = dsp.extract_json(srv_msg)
    print(srv_msg)
    length = len(srv_msg[1])
    messages = []
    for i in range(length):
      message = srv_msg[1][i]["message"]
      messages.append(message)
    for msg in messages:
      print(msg)
    # print(messages)
  
def request_unread(server, port, token):
  #Need token of User trying to read new messages they have gotten
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    req = dsp.req_new(token)
    client.connect((server, port))
    _send = client.makefile('w')
    recv = client.makefile('r')
    _send.write(req + '\r\n')
    _send.flush()
    srv_msg = recv.readline()
    srv_msg = dsp.extract_json(srv_msg)
    length = len(srv_msg[1])
    messages = []
    for i in range(length):
      message = srv_msg[1][i]["message"]
      messages.append(message)
    for msg in messages:
      print(msg)

# print(connect(HOST, PORT, usr, pwd))
# profile.load_profile('/Users/philip_bmn/Desktop/ICS32/final/marks.dsu')
# connect(HOST, PORT, profile.username, profile.password)
# send_message(HOST, PORT, token, 'pls work', 'dakuu')
# request_all(HOST, PORT, token)
# request_unread(HOST, PORT, token)