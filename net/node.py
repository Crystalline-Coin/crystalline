import sys,_thread
from flask import request,Flask
import flask
from flask.typing import ResponseValue
import requests
from peer import Peer
import time
#consts
MEDIUM="http://"

DEFAULT_PORT="5000"

FILE_NAME="code.txt"

REQUEST_HANDSHAKE="/hand_shake"

RECEIVE_DATA="/receive_data"

MY_IP_ADDRESS="" #ENTER 0.0.0.0 for public IP showing up  here
#consts

class Node:
    def __init__(self, ip_address, host_port=DEFAULT_PORT):
        self.ip_address=ip_address
        
        self.app=Flask(__name__)
        
        self.host_port=host_port
        
        self.peers=[]
        
        @self.app.route(REQUEST_HANDSHAKE, methods=['POST'])
        def request_handshake():  
            ip_address=request.remote_addr
            
            new_peer=Peer(request.form['port'], ip_address) #get the port and the ip address of the incoming node
            
            if (self.check_node_health(new_peer)):

                self.peers.append(new_peer) 
            
            else:
                
                return "<h1> Handshake Refused</h1> " , 400 
            

            return "<h1> Handshake response returned </h1>" , 200
        @self.app.route(RECEIVE_DATA, methods=['POST'])
        def recieve_data():

                print(request.form['data'])#deriving the data from post request , arbitrary function for testing data recievial ()
                                           #when you want to send me data you send it to this route and have a function tend to the data
                return  "Data received"# This won't show on the terminal ps just for fun( response code 200)
    def check_node_health(self, Peer):
        
        #Add other quality measurements here( Ping and stuff for Peers)
        #Just checks previous handshakes for now
     
        for peer in self.peers:
     
            if (peer.ip ==Peer.ip):
     
                return False
     
        return True
    def transmit(self, address_target, payload):              
        
        with self.app.app_context():
            requests.post(url=address_target,data=payload)           
    def send_async_data(self, peer, route ,payload):
            #we use this method to send our data, we specify the 
            #payload toinclude in the http payload and determine 
            #the  receiving end point host_port while providing the IP address and 
            #the recieving route (There are multiple ) receiving routes (/hand shake /receieve file )                                         
            #payload should be a dictionary in python format
            #keep in mind  running this function inside the main server thread, throttles and slows the app maybe even killing it 
            #you should initiate it inside a new thread 

            address=MEDIUM + peer.ip + ":" + peer.port + route #Forge the address

            try:

                _thread.start_new_thread(self.transmit, (address, payload))

            except:

                return " <h1> Data transmission failed </h1>", 400

            return " <h1> Data was  sent successfully </h1>" , 200
    def run_server(self):

            self.app.run(host=self.ip_address, port=DEFAULT_PORT)
