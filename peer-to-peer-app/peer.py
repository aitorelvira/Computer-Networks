# -*- coding: utf-8 -*-
""" The peer """

#from server import Server
from client import Client
from resource import Resource
from swarm import Swarm
import threading, socket

"""

define filePath with the torrent file path

"""

filePath = "C:/Users/Aitor/Desktop/Aitor/SF/Fall 2019/Computer Networks/Assignment 3/csc645-01-fall2019-projects-aitorelvira/applications/peer-to-peer-app/metainfo/config.torrent"



class Peer(Client):#, Server):
    # status
    PEER = 0
    SEEDER = 1
    LEECHER = 2
    PORT = 8000
    def __init__(self, max_upload_rate, max_download_rate, port = PORT):
        """
        TODO: implement the class constructor
        """
        #Server.__init__(self, port)
        Client.__init__(self, port)
        self.port = port
        self.status = self.PEER
        self.chocked = False
        self.interested = False
        self.max_download_rate = max_download_rate
        self.max_upload_rate = max_upload_rate
        self.print()


    def connect_to_tracker(self, ip_address, port):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((ip_address, port))
        return Swarm.peers()

    def connect_to_swarm(self, swarm):
        """
        TODO: implement this method
        This method will create a socket (TCP) connection
        with all the peers in the swarm sharing the requested
        resource.
        Take into consideration that even if you are connected
        to the swarm. You do not become a leecher until you set
        your status to interested, and at least one of the leechers
        or seeders in the swarm is not chocked.
        :param swarm: Swarm object returned from the tracker
        :return: VOID
        """
        pass  #Didn't have time to compute it

    def upload_rate(self, num_files):
        """
        TODO: implement this method
        Compute the actual upload rate using the formule from assignment docs
        This needs to be re-evaluated every 30 seconds approximatly
        :return: the new upload_rate
        """
        threading.Timer(30, self.download_rate()).start()
        uploadRate = self.max_upload_rate/num_files
        return uploadRate

    def download_rate(self):
        """
        TODO: implement this method
        Compute the actual download rate using the formule from assignment docs
        This needs to be re-evaluated every 30 seconds approximatly
        :return: the new download rate
        """
        threading.Timer(30, self.download_rate()).start()
        self.max_download_rate


        return self.max_download_rate #Didn't have time to finish it


    def get_metainfo(self, torrent_path):
        Resource.parse_metainfo(torrent_path)
        return Resource.announce

    def change_role(self, new_role):
        if self.interested():
            if self.unchocked():
                new_role = self.LEECHER
        if self.not_interested():
            new_role = self.SEEDER

    def send_message(self, block, start_index = -1, end_index = -1):
        """
        TODO: implement this method
        (1) Create a message object from the message class
        (2) Set all the properties of the message object
        (3) If the start index and end_index are not negative
            then, that means that the block needs to be sent
            in parts. implement that situations too.
        (4) Don't forget to check for exceptions with try-catch
            before sending messages. Also, don't forget to
            serialize the message object before being sent
        :param block: a block object from the Block class
        :param start_index: the start index (if any) of the data being sent
        :param end_index: the end index of the data being sent
        :return: VOID
        """
        pass

    def recieve_message(self):
        """
        TODO: implement this method
        (1) recieve the message
        (2) inspect the message (i.e does it have payload)
        (4) If this was the last block of a piece, then you need
            to compare the piece with the sha1 from the torrent file
            if is the same hash, then you have a complete piece. So, set
            the piece object related to that piece to completed.
        (5) Save the piece data in the downloads file.
        (6) Start sharing the piece with other peers.
        :return: VOID
        """
        pass

    def get_top_four_peers(self):
        """
        TODO: implement this method
        Since we are implementing the 'tit-for-tat' algorithm
        which upload data to the top 4 peers in the swarm (max rate upload peers)
        then this method will inspect the swarm object returned by the tracker
        and will get the 4 top peers with highest upload rates. This method needs to
        be re-evaluated every 30 seconds.
        :return: a list of the 4 top peers in the swarm
        """
        self.top_four = []
        # your implementation here
        return self.top_four

    def verify_piece_downloaded(self, piece):
        """
        TODO: implement this method
        :param piece: the piece object of this piece
        :return: true if the piece is verified and is not corrupted, otherwisem, return false
        """
        return False

    def is_chocked(self):
        return self.chocked

    def is_interested(self):
        return self.interested

    def chocked(self):
        self.chocked = True

    def unchocked(self):
        self.chocked = False

    def interested(self):
        self.interested = True

    def not_interested(self):
        self.interested = False
    def print(self):
        print("Peer info: id: "+ self.PEER + ", IP: " + self.PORT)
        print("Max download rate: " + self.download_rate() + "b/s")
        print("Max upload rate: " + self.upload_rate() + "b/s")
        print("*** Downloads in progress ***")
        print("-File " + Resource.getFileName(filePath) + "total downloaded: ")
        print("*** Uploads in progress ***")
        print("-File " + Resource.getFileName(filePath) + "total uploaded: ")