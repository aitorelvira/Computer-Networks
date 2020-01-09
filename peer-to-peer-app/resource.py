# -*- coding: utf-8 -*-
""" The Resource, Piece and Block classes
This file contains the classes Resource, Piece and Block to provide
services and functionalities needed from a resource in a swarm.
"""
import hashlib



"""

define filePath with the torrent file path

"""

filePath = "C:/Users/Aitor/Desktop/Aitor/SF/Fall 2019/Computer Networks/Assignment 3/csc645-01-fall2019-projects-aitorelvira/applications/peer-to-peer-app/metainfo/config.torrent"




class Resource(object):
    """
    This class provides services to handle resources
    """

    def __init__(self, resource_id = 0, file_path = None, file_len = 0, piece_len = 0 ):
        """
        TODO: complete the implementation of this constructor.
        :param resource_id: default 0
        :param file_path: default None
        :param file_len: default 0
        :param piece_len: default 0
        """
        self.file_path = file_path
        self.resource_id = resource_id
        self.len = file_len
        self.max_piece_size = piece_len
        self.trackers = []
        self.completed = []  # the pieces that are already completed

    def add_tracker(self, ip_address, port):
        announce = "announce:" + str(ip_address) + ":" + str(port)
        self.trackers.append(announce)
        return announce

    def get_trackers(self):
        return self.trackers

    def len(self):
        return self.len

    def name(self, path):
        return self.getFileName(path)

    def _create_pieces(self, file_len, piece_len):
        pieceNum = file_len / piece_len
        self.pieces = [] # list of objects of pieces. (see Piece class)
        self.pieces.append(pieceNum)
        print(str(self.pieces))

    def get_piece(self, index):
        return self.pieces[index]

    def sha1_hashes(self):
        hashes = []
        for piece in self.pieces:
            hash = Piece._hash_sha1(piece)
            hashes.append(hash)
        return hashes

    def parse_metainfo(self, file_path):
        info = {
            "file_name": self.getFileName(file_path),
            "piece_length": self.getPieceLength(file_path),
            "length": self.getLength(file_path),
            "pieces": self.getPieces(file_path)
        }

        announce = {
                "announce": self.getIPAddress(file_path) + ":" + self.getPort(file_path),
                "info": info
        }
        
        print(announce)
        return announce

    def getIPAddress(self, filePath):
        count = 0
        IPAddress = []
        aux = 0
        dots = 0
        fileIPAddress = ""
        with open(filePath) as fp:
            for line in fp:
                for ch in line:
                    if count == 0:
                        if ch == ":":
                            dots = dots + 1
                        if dots == 1:
                            IPAddress.append(ch)
                    aux = aux + 1
                count = count + 1
        n = 3
        while n < IPAddress.__len__():
            fileIPAddress = fileIPAddress + str(IPAddress[n])
            n = n + 1
        return fileIPAddress

    def getPort(self, filePath):
        count = 0
        port = []
        aux = 0
        dots = 0
        filePort = ""
        with open(filePath) as fp:
            for line in fp:
                for ch in line:
                    if count == 0:
                        if ch == ":":
                            dots = dots + 1
                        if dots == 2:
                            port.append(ch)
                    aux = aux + 1
                count = count + 1
        n = 1
        while n < port.__len__() - 3:
            filePort = filePort + str(port[n])
            n = n + 1
        return filePort

    def getFileName(self, filePath):
        count = 0
        name = []
        fileName = ""
        with open(filePath) as fp:
            for line in fp:
                for ch in line:
                    if count == 1:
                        name.append(ch)
                count = count + 1
        n = 9
        while n < name.__len__() - 3:
            fileName = fileName + str(name[n])
            n = n + 1
        return fileName

    def getPieceLength(self, filePath):
        count = 0
        length = []
        pieceLength = ""
        with open(filePath) as fp:
            for line in fp:
                for ch in line:
                    if count == 2:
                        length.append(ch)
                count = count + 1
        n = 16
        while n < length.__len__() - 2:
            pieceLength = pieceLength + length[n]
            n = n + 1
        return pieceLength

    def getLength(self, filePath):
        count = 0
        length = []
        varLength = ""
        with open(filePath) as fp:
            for line in fp:
                for ch in line:
                    if count == 3:
                        length.append(ch)
                count = count + 1
        n = 10
        while n < length.__len__() - 2:
            varLength = varLength + length[n]
            n = n + 1
        return varLength

    def getPieces(self, filePath):
        count = 0
        pieces = []
        filePieces = ""
        with open(filePath) as fp:
            for line in fp:
                for ch in line:
                    if count == 4:
                        pieces.append(ch)
                count = count + 1
        n = 10
        while n < pieces.__len__():
            filePieces = filePieces + pieces[n]
            n = n + 1
        return filePieces

resource = Resource()
resource._create_pieces(int(resource.getLength(filePath)), int(resource.getPieceLength(filePath)))
resource.parse_metainfo(filePath)

class Piece(object):
    """
    This class provides the services needed to handle pieces from a resource (file)
    """
    def __init__(self, data, piece_id, resource_id):
        self.data = data
        self.resource_id = resource_id
        self.piece_id = piece_id
        self._create_blocks()
        self.hash = self._hash_sha1()
        self.completed = False


    def _create_blocks(self, max_size = 16):
        convertedSize = max_size * 1024
        numBlocks = convertedSize / 256
        self.blocks = []
        self.blocks.append(numBlocks)
        return self.blocks

    def _hash_sha1(self, data = None):
        if not data:
            data = self.data
        hash_object = hashlib.sha1(data.encode())
        return hash_object.hexdigest()

    def get_hash(self):
        return self.hash

    def is_equal_to(self, piece):
        for piece in resource.pieces:
            if self._hash_sha1(piece) == resource.hashes:
                self.set_to_complete()
            else:
                resource.getPieces(filePath)

    def get_blocks(self):
        return self.blocks

    def is_completed(self):
        return self.completed

    def set_to_complete(self):
        self.completed = True


class Block(object):
    """
    This class implements all the services provided by a block from piece
    """
    def __init__(self, block_id, piece_id, resource_id):
        self.resource_id = resource_id
        self.piece_id = piece_id
        self.block_id = block_id

    # TODO: think about which methods you would implement in this class.


