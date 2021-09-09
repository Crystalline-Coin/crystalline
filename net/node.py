import sys, _thread
from flask import request, Flask
import flask
from flask.typing import ResponseValue
import requests
from peer import peer

# consts
MEDIUM = "http://"

DEFAULT_PORT = "5000"

FILE_NAME = "code.txt"

HANDSHAKE_RESPONSE = "/respond_handshake"

REQUEST_HANDSHAKE = "/hand_shake"

RECEIVE_DATA = "/receive_data"

MY_IP_ADDRESS = ""  # ENTER 0.0.0.0 for public IP showing up  here


# consts

class Node:
    def __init__(self, ip_address, host_port=DEFAULT_PORT):

        self.ip_address = ip_address

        self.app = Flask(__name__)

        self.host_port = host_port

        self.peers = []

        @self.app.route(REQUEST_HANDSHAKE, methods=['POST'])
        def request_handshake():

            ip_address = request.remote_addr

            handshake_data = {'port': self.host_port}  # fill this for future handshake implementations
            # for now it's filled with sender open port
            new_peer = Peer(request.form['port'], ip_address)  # get the port and the ip address of the

            if (self.check_node_health(new_peer)):

                self.peers.append(new_peer)

            else:

                return "Handshake Refused"  # working on returning code based response ( Like 404 or 500 series errors)

            _thread.start_new_thread(self.send_async_data, (ip_address, HANDSHAKE_RESPONSE, request.form['port'],
                                                            handshake_data))  # Send the data of our host_port to the other Peer

            return "Handshake handling response returned"

        @self.app.route(HANDSHAKE_RESPONSE, methods=['POST'])
        def respond_handshake():

            return "Handshake done"

        @self.app.route(RECEIVE_DATA, methods=['POST'])
        def receive_data():

            print(request.form[
                      'data'])  # deriving the data from post request , arbitrary function for testing data receival ()
            # when you want to send me data you send it to this route and have a function tend to the data

            return "Data received"  # This won't show on the terminal ps just for fun( response code 200)

    def check_node_health(self, Peer):

        # Add other quality measurements here( Ping and stuff for Peers)

        # Just checks previous handshakes for now

        for peer in self.peers:

            if (peer.ip == Peer.ip):
                return False

        return True

    def send_async_data(self, ip_address, route, port, payload):
        # we use this method to send our data, we specify the
        # payload toinclude in the http payload and determine
        # the  receiving end point host_port while providing the IP address and
        # the receiving route (There are multiple ) receiving routes (/hand shake /receieve file )
        # payload should be a dictionary in python format
        # keep in mind  running this function inside the main server thread, throttles and slows the app maybe even killing it
        # you should initiate it inside a new thread
        address = MEDIUM + ip_address + ":" + port + route  # Forge the address

        try:
            with self.app.app_context():

                requests.post(address, data=payload)

        except:

            print("Request was not sent succesfully ")

        return "Data was  sent successfully"

    def run_server(self):
        self.app.run(host=self.ip_address, port=int(DEFAULT_PORT))
