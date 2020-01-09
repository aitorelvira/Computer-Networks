# -*- coding: utf-8 -*-
""" The tracker
This file implements the Tracker class. The tracker has two main functionalities
 (1) A client connects to a tracker, and a tracker sends
all the peers ip addresses and ports connected to the swarm that are sharing
the same resource. Since a tracker can handle more than one swarm, then the
swarm needs to be identified with a id (i.e the file id that is being shared
in the swarm)
 (2) When a peers change status (become leechers or seeders) they must inform
 the tracker, so the tracker can update that info in the swarm where they are
 sharing the resource

"""
from server import Server
from swarm import Swarm
from peer import Peer


class Tracker(Server):

    PORT = 12000
    IP_ADDRESS = "127.0.0.1"

    def __init__(self, ip_address = IP_ADDRESS, port = PORT):
        """
        TODO: finish constructor implementation (if needed)
        If parameters ip_address and port are not set at the object creation time,
        you need to use the default IP address and the default port set in the class constants.
        :param ip_address:
        :param port:
        """
        self.port = port
        Server.__init__(self, port)
        self.ip = ip_address
        # the list of swarms that this tracker keeps
        self.swarms = []

    def add_swarm(self, swarm):
        self.swarms.append(swarm)

    def remove_swarm(self, resource_id):
        for swarm in self.swarms:
            if self.swarms(swarm).resource_id == resource_id:
                self.swarms.remove(swarm)

    def add_peer_to_swarm(self, peer, resource_id):
        for swarm in self.swarms:
            if self.swarms(swarm).resource_id == resource_id:
                Swarm.add_peer(peer)

    def change_peer_status(self, resource_id):
        Peer.change_role()

    def send_peers(self, peer_socket, resource_id):

        for swarm in self.swarms:
            if self.swarms(swarm).resource_id == resource_id:
                Server.send(peer_socket)
tracker = Tracker.__init__("localhost", 12000)