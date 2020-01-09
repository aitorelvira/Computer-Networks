# -*- coding: utf-8 -*-
""" The client
This file has the class client that implements a client socket.
Note that you can replace this client file by your client from
assignment #1.
"""
import socket
import pickle


class Client(object):


    def __init__(self, port):
        self.port = port
        self.init_client()
        self.connect('localhost', port)


    def init_client(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except socket.error as err:
            print("Error while creating client socket" + str(err))

    def connect(self, ip_adress, port):
        try:
            self.client_socket.connect((ip_adress, port))
            self.send({"client_name": "Mark"})
        except socket.error as err:
            print("Error while connecting to server" + str(err))
    def send(self, data):
        try:
            data_serialized = pickle.dumps(data)
            self.client_socket.send(data_serialized)
            self.recieve(1024)
        except socket.error as err:
            print("Error while sending request to server" + str(err))

    def recieve(self, memory_allocation_size):
        while True:
            received_response = self.client_socket.recv(memory_allocation_size)
            received_data = pickle.loads(received_response)
            print("Form server: " + str(received_data))
        self.close()
    def close(self):
        self.client_socket.close()

client =  Client(9000)