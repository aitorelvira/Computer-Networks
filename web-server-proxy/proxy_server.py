import os
from threading import Thread
import sys
import socket
from proxy_thread import ProxyThread


class ProxyServer(object):

    HOST = '127.0.0.1'
    PORT = 12000
    BACKLOG = 50
    MAX_DATA_RECV = 4096

    try:
        global server_socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
    except socket.error as err:
        print("Error while creating socket" + str(err))

    def __init__(self):
        self.clients = []
        self.run()

    def run(self):
        host = 'localhost'
        port = 12000
        max_num_connections = 5
        try:
            server_socket.bind((host, port))  # associate the socket to host and port
            print("Server listening at port..." + str(port))
        except socket.error as err:
            print("Error while binding socket" + str(err))
        while True:
            try:
                server_socket.listen(max_num_connections)  # listen and accept clients
                connection, address = server_socket.accept()
                self.proxy_thread(connection, address)
                connection.close()
                server_socket.close()
            except socket.error as err:
                print("Error while accepting socket" + str(err))

    def proxy_thread(self, conn, client_addr):
        """
        I made this method for you. It is already completed and no need to modify it. 
        This already creates the threads for the proxy is up to you to find out where to put it.
        Hint: since we are using only  non-persistent connections. Then, when a clients connects, 
        it also means that it already has a request to be made. Think about the difference 
        between this and assign#1 when you created a new thread. 
        :param conn: 
        :param client_addr: 
        :return:
        """
        proxy_thread = ProxyThread(conn, client_addr)
        proxy_thread.init_thread()


server = ProxyServer()
server.run()
