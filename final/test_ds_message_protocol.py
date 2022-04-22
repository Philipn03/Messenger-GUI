import unittest
import ds_client as dsc

usr = 'herr'
pwd = 'password123'
HOST = '168.235.86.101'
PORT = 3021
token = '3199cde1-b404-40eb-a9a9-22426d202f5e'
send_message = '{"response": {"type": "ok", "message": "Direct message sent"}}\n'
request_all = "{'response': {'type': 'error', 'message': 'Unable to decrypt post entry.'}}"

class test_dsc(unittest.TestCase):
    def test_connect_Test(self):
        self.assertEqual(dsc.connect(HOST, PORT, usr, pwd), token)

    def test_send_message_Test(self):
        self.assertEqual(dsc.send_message(HOST, PORT, token, 'dakuu'), send_message)

    def test_request_all_Test(self):
        self.assertNotEqual(dsc.request_all(), request_all)

    def test_request_new_Test(self):
        pass

if __name__ == '__main__':
    unittest.main()