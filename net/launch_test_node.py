FILE_NAME="code.txt"

HANDSHAKE_RESPONSE="/respond_handshake"

REQUEST_HANDSHAKE="/hand_shake"

RECEIVE_DATA="/receive_data"

DEFAULT_PORT="5000"

MY_IP_ADDRESS="//.//.//.//" #ENTER 0.0.0.0 for public IP showing up  here
#consts
#run this in a seperate terminal than test.py!
LOCAL_HOST="//.//.//.//" #enter your private IP address here ( or public who cares)
from node import *
new_node=Node(ip_address=LOCAL_HOST,host_port=DEFAULT_PORT)
new_node.run_server()
