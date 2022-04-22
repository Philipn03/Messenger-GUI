# Philip Nguyen
# philipbn@uci.edu
# 57277528

import socket
import ds_protocol as dsp
from Profile import Profile
from pathlib import Path

HOST = '168.235.86.101'
PORT = 3021

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None

class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
    try:
      token = self.connect()
      self.token = token
    except:
      self.token = None

  def connect(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      join_msg = dsp.join(self.username, self.password)
      client.settimeout(1)
      client.connect((self.dsuserver, 3021))
      _send = client.makefile('w')
      recv = client.makefile('r')
      _send.write(join_msg + '\r\n')
      _send.flush()
      srv_msg = recv.readline()
      try:
        x = dsp.extract_token(srv_msg)
        print(x)
        token = x.token
      except:
        token = None
      return token

  def send(self, message:str, recipient:str) -> bool:
    # returns true if message successfully sent, false if send failed
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        msg = dsp.send_msg(self.token, message, recipient)
        client.connect((self.dsuserver, 3021))
        _send = client.makefile('w')
        recv = client.makefile('r')
        _send.write(msg + '\r\n')
        _send.flush()
        srv_msg = recv.readline()
        if srv_msg[23:28] == 'error':
          return False
        else:
          return True
    except:
      return False

  def retrieve_new(self) -> list:
    # returns a list of DirectMessage objects containing all new messages
    directmessage = DirectMessage
    # directmessage.recipient = 
    # directmessage.message = 
    # directmessage.timestamp =
    #Need token of User trying to read new messages they have gotten
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      req = dsp.req_new(self.token)
      client.connect((self.dsuserver, 3021))
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
      return messages
 
  def retrieve_all(self) -> list:
    # returns a list of DirectMessage objects containing all messages
    directmessage = DirectMessage
    # directmessage.recipient = 
    # directmessage.message = 
    # directmessage.timestamp =
    #Need token of User trying to read all messages they have gotten
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      req = dsp.req_all(self.token)
      client.connect((self.dsuserver, 3021))
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
      return messages

# dm = DirectMessenger('168.235.86.101', 'dakuu', 'Manny')