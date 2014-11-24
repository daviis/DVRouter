'''
Created on Nov 6, 2014

@author: daviis01

A basic class that just camps a socket pushing everything it gets onto the queue.
'''
import socket
from threading import Thread

class SockReader(Thread):
    
    def __init__(self, queue):
        Thread.__init__(self)
        self.q = queue
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(("", 50007))
        
    def run(self):
        while True:
            pkt, _ = self.s.recvfrom(2048)
            self.q.put(pkt)
            
