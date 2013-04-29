#!/usr/bin/python


import dbc_client3, \
    sys

username='dguerchu'
password='30654815'
if len(sys.argv) < 2:
    sys.exit()
    
client = dbc_client3.Client(username, password)
balance = client.get_balance()
try :
    id, text = client.decode( sys.argv[1])
except Exception as e:
    print e
else:
    print text

