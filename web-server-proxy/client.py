import socket
import pickle
import requests


class Client(object):
    """
    This class represents your client class that will send requests to the proxy server and will hand the responses to 
    the user to be rendered by the browser, 
    """
    try:
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("Error while creating client socket" + str(err))

    def __init__(self, data):
        self.init_socket()
        self._connect_to_server('localhost', 12000)
        self._send(data)
        #self._receive() Function commented as I did not get to implement the response of the server
        self.request_to_proxy(data)

    def init_socket(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket successfully created")
        except socket.error as err:
            print("socket creation failed with error %s" % (err))

    def _connect_to_server(self, host_ip, port):
        try:
            self.host_ip = host_ip
            self.port = port
            client_socket.connect((host_ip, port))
        except socket.error as err:
            print("Error while connecting to proxy server" + str(err))

    def _send(self, data):
        try:
            data_serialized = pickle.dumps(data)
            client_socket.send(data_serialized)
        except socket.error as err:
            print("Error while sending request to proxy server" + str(err))

    def _receive(self):
        """
        1. Implements the primitive rcv() method from socket
        2. Desirialize data after it is recieved
        :return: the desirialized data 
        """
        while True:
            try:
                proxy_server_response = client_socket.recv(4096)
                proxy_server_data = pickle.loads(proxy_server_response)
                global url
                url = proxy_server_data["url"]
                global is_private_mode
                is_private_mode = proxy_server_data["private_mode"]

            except socket.error as err:
                print("Error while getting response from proxy server" + str(err))
            return proxy_server_data
        client_socket.close()

    def request_to_proxy(self, data):
        """
        Create the request from data 
        request must have headers and can be GET or POST. depending on the option
        then send all the data with _send() method
        :param data: url and private mode 
        :return: VOID
        """
        web_url = "http://" + data["url"]
        parameters = {"is_private_mode": data["is_private_mode"]}
        r = requests.get(url = web_url, params = parameters)
        #dataToText = r.json()
        letra = r.url
        i = 7
        newUrl = ""
        newMode = ""
        while i < letra.__len__():
            if letra[i] == '?':
                endUrl = i
                newMode = letra[letra.__len__() - 1]
                break
            newUrl = newUrl + letra[i]
            i = i + 1
        j = endUrl + 1
        aux = newUrl.__len__() - 1
        newData = {'url': newUrl[0:aux], 'is_private_mode': int(newMode)}
        self._send(newData)


    def response_from_proxy(self):
        """
        the response from the proxy after putting the _recieve method to listen.
        handle the response, and then render HTML in browser. 
        This method must be called from web_proxy_server.py which is the home page of the app
        :return: the response from the proxy server
        """
        return 0
