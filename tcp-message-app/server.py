import socket
import threading
import pickle

MAX_NUM_CONNECTIONS = 5
threads = []
lock = threading.Lock()


class Server:
    try:
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Declaration of the server socket
    except socket.error as err:
        print("Error while creating server socket" + str(err))

    @staticmethod
    def bind_socket(host, port):
        try:
            server.bind((host, port))
            print("Server Info\nIP Address: " + host + "\nport listening: " + str(port) + "\nWaiting for connections...")
        except socket.error as err:
            print("Error while binding socket" + str(err))

    @staticmethod
    def accept_socket(host, port):
        while True:
            try:
                server.listen(MAX_NUM_CONNECTIONS)
                connection, address = server.accept()
                client_id = address[1]
                lock.acquire()
                thread = threading.Thread(target=Server.run_thread(connection, client_id))  # Create the thread that is going to interact with the client
                thread.start()
                threads.append(thread)
                connection.close()  # Close the connection so more clients can connect with the server
            except socket.error as err:
                print("Error while accepting socket")
        server.close()


    @staticmethod
    def run_thread(connection, client_id):
        first_time = True
        #loop = True
        while True:
            request_from_client = connection.recv(4096)
            data = pickle.loads(request_from_client)  # Deserializes the data
            client_num = data["num"]  # Gets the parameter that the client has introduced
            if client_num == 0 and first_time:  # Prints that the client has connected to the server
                client_name = data["client_name"]
                print("Client: " + client_name + " with clientid: " + str(client_id) + " has connected to this server")
                first_time = False
            if client_num == 1:
                print("List of users sent to client: " + str(client_id))
            if client_num == 2:
                user_id = data["user_id"]
                print("List of messages sent to " + str(user_id))
            if client_num == 3:
                print("You, " + str(client_id) + " have recived your list of messages")
            if client_num == 4:
                print("Client " + str(client_id) + " has created a new channel")
            if client_num == 5:
                print("Userid: " + str(client_id) + " connected to the channel")
            if client_num == 6:
                print("Client " + str(client_id) + " disconnected from server")
                server_msg = "Hello from server!"
                server_response = {"client_id": client_id, "msg_from_server": server_msg}
                # serialize and sent the data to client
                encrypted_data = pickle.dumps(server_response)
                connection.send(encrypted_data)
                lock.release()
                break
                #loop = False
            server_msg = "Hello from server!"
            server_response = {"client_id": client_id, "msg_from_server": server_msg}
            # serialize and sent the data to client
            encrypted_data = pickle.dumps(server_response)
            connection.send(encrypted_data)
        connection.close()

    for i in threads:
        i.join()

    """
    @staticmethod
    def run_thread(connection, client_id):
        print("entro run thread")
        loop = True
        print(loop)
        while True:
            request_from_client = connection.recv(4096)
            data = pickle.loads(request_from_client)  # Deserializes the data
            client_num = data["num"]  # Gets the parameter that the client has introduced
            if client_num == 0:  # Prints that the client has connected to the server
                client_name = data["client_name"]
                print("Client: " + client_name + " with clientid: " + str(client_id) + " has connected to this server")
            if client_num == 1:
                print("List of users sent to client: " + str(client_id))
            if client_num == 2:
                client_id = data["user_id"]
                print("List of messages sent to " + str(client_id))
            if client_num == 3:
                print("You, " + str(client_id) + " have recived your list of messages")
            if client_num == 4:
                print("Client " + str(client_id) + " has created a new channel")
            if client_num == 5:
                print("Userid: " + str(client_id) + " connected to the channel")
            if client_num == 6:
                print("Client " + str(client_id) + " disconnected from server")
                server_msg = "Hello from server!"
                server_response = {"client_id": client_id, "msg_from_server": server_msg}
                # serialize and sent the data to client
                encrypted_data = pickle.dumps(server_response)
                connection.send(encrypted_data)
                print("Connection sent1")
                break
            server_msg = "Hello from server!"
            server_response = {"client_id": client_id, "msg_from_server": server_msg}
            # serialize and sent the data to client
            encrypted_data = pickle.dumps(server_response)
            connection.send(encrypted_data)
            print("Connection sent2")
    """



myServer = Server()
myServer.bind_socket('localhost', 9999)
myServer.accept_socket('localhost', 9999)