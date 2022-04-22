# ds_protocol.py
# Simar Cheema
# simarc@uci.edu
# 31075859

import json
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['type','token_or_message'])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  DataTuple = namedtuple('DataTuple', ['type','messages'])
  try:
    json_obj = json.loads(json_msg)
    type = json_obj['response']['type']
    messages = json_obj['response']['messages']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
  return DataTuple(type, messages)

def extract_token(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  DataTuple = namedtuple('DataTuple', ['type','token'])
  try:
    json_obj = json.loads(json_msg)
    type = json_obj['response']['type']
    token = json_obj['response']['token']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
  return DataTuple(type, token)

def join(usr, pwd):
  join_msg = '{"join": {"username": ' + '"' + usr + '"' + ',"password": ' + '"' + pwd + '"' + ', "token":""}}'
  return join_msg

def send_msg(token, msg, recipient):
  send = '{"token":"' + token + '", "directmessage": {"entry": ' + '"' + msg + '"' + ',"recipient":' + '"' + recipient + '"' + ', "timestamp": "1603167689.3928561"}}'
  return send

def req_all(token):
  req = '{"token":' + '"' + token + '"' + ', "directmessage": "all"}'
  return req

def req_new(token):
  req = '{"token":' + '"' + token + '"' + ', "directmessage": "new"}'
  return req