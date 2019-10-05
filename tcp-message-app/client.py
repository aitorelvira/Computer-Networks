import socket
import pickle
import datetime
import threading


class TCPClientHandler:

    @staticmethod
    def get_host():
        host = input("Enter the server IP Address: ")
        return host

    @staticmethod
    def get_port():
        port = int(input("Enter the server port: "))
        return port

    @staticmethod
    def get_name():
        client_name = input("Your id key (i.e your name): ")
        return client_name

    @staticmethod
    def options():
        print("****** TCP Message App ******\n-----------------------")
        print("Options Available:")
        print("1. Get user list ")
        print("2. Sent a message")
        print("3. Get my message")
        print("4. Create a new channel")
        print("5. Chat in a channel with your friends")
        print("6. Disconnect from server\n\n")

    global message_list, date_list
    message_list = []
    date_list = []
    @staticmethod
    def get_answer():  # Gets the answer that the client introduce
        answer = input("Your option <enter a number>")
        print("--------------------------------")
        if answer == '1':
            print(client_list)
            TCPClientHandler.send_answer1()
        if answer == '2':
            global user_message, user_id
            user_message = input("Your message: ")
            message_date = datetime.datetime.now()
            message_list.append(user_message)
            date_list.append(message_date)
            user_id = input("User ID recipent: ")
            print("Message sent!")
            TCPClientHandler.send_answer2()
        if answer == '3':
            print("My messages:")
            i = 0
            for i in range(len(message_list)):
                #if client_id == user_id:
                 print(str(date_list[i]) + ": " + message_list[i] + " (from: " + client_name + ")")
            TCPClientHandler.send_answer3()
        if answer == '4':
            print("----------------------- Channel ------------------------")
            new_host = input("Enter the ip address for the new channel: ")
            new_port = int(input("Enter the port to listen for new users: "))
            print("Channel Info\nIP Address: " + new_host + "\nChannel clientid: " + str(new_port) +"\nWaiting for users....")
            new_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_client.connect((new_host, new_port))
            TCPClientHandler.send_answer4()
        if answer == '5':
            print("Enter Bye to exit the channel")
            TCPClientHandler.send_answer5()
        if answer == '6':
            TCPClientHandler.send_answer6()

    @staticmethod
    def send_answer1():
        try:
            answer1 = {"client_name": client_name, "num": 1}
            answer1_serialized = pickle.dumps(answer1)
            client.send(answer1_serialized)
        except socket.error as err:
            print("Error while sending answer 1")

    @staticmethod
    def send_answer2():
        try:
            answer2 = {"user_message": user_message, "user_id": str(user_id), "date": datetime.date, "user_name": client_name, "num": 2}
            answer2_serialized = pickle.dumps(answer2)
            client.send(answer2_serialized)
        except socket.error as err:
            print("Error while sending answer 2")

    @staticmethod
    def send_answer3():
        try:
            if len(message_list) == 0:
                print("There is no more messages for you")
            answer3 = {"num": 3}
            answer3_serialized = pickle.dumps(answer3)
            client.send(answer3_serialized)
        except socket.error as err:
            print("Error while sending answer 3")

    @staticmethod
    def send_answer4():
        try:
            answer4 = {"num": 4}
            answer4_serialized = pickle.dumps(answer4)
            client.send(answer4_serialized)
        except socket.error as err:
            print("Error while sending answer 4")

    @staticmethod
    def send_answer5():
        try:
            answer5 = {"num": 5}
            answer5_serialized = pickle.dumps(answer5)
            client.send(answer5_serialized)
        except socket.error as err:
            print("Error while sending answer 5")

    @staticmethod
    def send_answer6():
        try:
            answer6 = {"num": 6}
            answer6_serialized = pickle.dumps(answer6)
            client.send(answer6_serialized)
        except socket.error as err:
            print("Error while sending answer 6")


myClientHandler = TCPClientHandler()
host = myClientHandler.get_host()
port = myClientHandler.get_port()
client_name = myClientHandler.get_name()

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("Error while creating client socket" + str(err))


class Client:
    @staticmethod
    def connect_to_server():
        try:
            client.connect((host, port))
        except socket.error as err:
            print("Error while connecting to server" + str(err))

    @staticmethod
    def send_request():
        try:
            data = {"client_name": client_name, "num": 0}
            data_serialized = pickle.dumps(data)
            client.send(data_serialized)
        except socket.error as err:
            print("Error while sending request to server" + str(err))

    @staticmethod
    def retrieve_response():
        first_time = True
        first_name = True
        global client_list
        client_list = []
        while True:
            try:
                server_response = client.recv(4096)
                server_data = pickle.loads(server_response)
                global client_id
                client_id = server_data['client_id']
                if first_name:  # It should only add the client once
                    client_list.append(client_name)
                    first_name = False
                server_msg = server_data['msg_from_server']
                if first_time:  # It should only print those messages once
                    print("Successfully connected to server with IP: " + str(host) + " and port: " + str(port))
                    print("Your client info is:")
                    print("Client Name: " + client_name)
                    print("Client ID: " + str(client_id) + "\n\n")
                    first_time = False
                myClientHandler.options()
                myClientHandler.get_answer()
            except socket.error as err:
                print("Error while retrieving socket's response" + str(err))
        client.close()


myClient = Client()
myClient.connect_to_server()
myClient.send_request()
myClient.retrieve_response()