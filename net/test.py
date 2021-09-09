MEDIUM="http://"

DEFAULT_PORT="5000"
import requests
import time
FILE_NAME="code.txt"

HANDSHAKE_RESPONSE="/respond_handshake"

REQUEST_HANDSHAKE="/hand_shake"

RECEIVE_DATA="/receive_data"

MY_IP_ADDRESS="//.//.//.//" #ENTER 0.0.0.0 for public IP showing up  here
#consts
#run this in a seperate terminal than launch node!
LOCAL_HOST="//.//.//.//" #enter your private IP address here ( or public who cares)
def test_hand_shake():
    #test for handshake on your own local host send a handshake request to your self and get the response
    while(True):    
      
            if (requests.post(MEDIUM+LOCAL_HOST+":"+DEFAULT_PORT+REQUEST_HANDSHAKE,data={"port":DEFAULT_PORT}).status_code==400):
         
                print("Handshake refused because of succession ")
                break


test_hand_shake()