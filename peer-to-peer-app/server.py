# -*- coding: utf-8 -*-
""" The server
This file has the class client that implements a server socket.
Note that you can replace this server file by your server from
assignment #1.
"""
import socket
import pickle
import threading


class Server(object):

    def __init__(self, port):
        self.port = port
        self.init_server()
        self.listen(port)
        #self.threaded_client()


    def init_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("Error while creating server socket" + str(err))


    def listen(self, port):
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(1)
        self.accept()

    def accept(self):
        while True:
            connection, address = self.server_socket.accept()
            self.recieve(1024, connection)
        connection.close()
        return

    def recieve(self, memory_allocation_size, connection):
        received_response = connection.recv(memory_allocation_size)
        received_data = pickle.loads(received_response)
        print("Form client: " + str(received_data))
        self.send({"server_name": "Alex"}, connection)
        return received_data

    def send(self, data, connection):
        try:
            data_serialized = pickle.dumps(data)
            connection.send(data_serialized)
        except socket.error as err:
            print("Error while sending data to client" + str(err))

    def threaded_client(self, conn, client_addr):
        """
        TODO: implement this method
        :param conn:
        :param client_addr:
        :return: a threaded client.
        """

        return None

server = Server(9000)



