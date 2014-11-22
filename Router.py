"""
@author:Isaac Davis
@date: 2014-11-05
"""
import sys
import Table
import json
import socket
from threading import Thread

class Router(Thread):
    
    def __init__(self, aFile, qu):
        """
        Init a Router obj with aFile uri, a builting locking queue, and someName that represents my router
        """
        Thread.__init__(self)
        self.q = qu
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", 50008))
        
        try:
            self.table, self.myName = self._makeInitialTable(aFile)
        except IOError:
            print("File ", aFile, " does not exist", sys.stderr)
            
    def _makeInitialTable(self, aFile):
        """
        Take a file's uri, open it and read it into my Table object
        """
        someFile = open(aFile, 'r')
        initTable = Table.Table() 
        myName = ""
        for line in someFile:
            stripLine = line.strip()
            name, cost, ip = stripLine.split(" ")
            cost = int(cost)
            if cost == 0:
                myName = name
                initTable.addSelf(name)
            else:
                ipStrip = ip.rstrip()
                initTable.addNeighbor(name, cost, ipStrip)
        someFile.close()
        return (initTable, myName)
    
    def run(self):
        """
        The part of the thread that will continually execute. It pulls something off of the queue or it will block unitll there is something. 
        Then it decides on the messages type. And either updates it table (which may or may not trigger an update), prints out a message, or forwards
        a message.
        """
        print(self.table)
        self.sendUpdates()
        self.sendRestart()
        while True:
            pkt = self.q.get()
            fullMsg = json.loads(pkt.decode('utf-8'))
            if fullMsg['type'] == "table":
                print("incoming table from: ", fullMsg['source'], " full msg: ", fullMsg)
                if self.checkIncomingUpdate(fullMsg['table'], fullMsg['source']):
                    print(self.table)
                    self.sendUpdates()
                #else there was no update so no need to update neighbors
            elif fullMsg['type'] == "message":
                if self.amReciver(fullMsg):
                    print(fullMsg['source'], " says ", fullMsg['message']['content'])
                else:
                    updatedMsg, nextIp = self.forwardMsg(fullMsg)
                    self.sock.sendto(updatedMsg, (nextIp, 50007))
                #send it on
            elif fullMsg['type'] == 'printTable':
                print(self.table)
            elif fullMsg['type'] == 'restart':
                self.sendUpdates()
            else:
                print("type field of ", fullMsg['type'], " unknown from incoming json")
            
    def amReciver(self, msg):
        if msg['message']['destination'] == self.myName:
            return True
        else:
            return False
        
    def checkIncomingUpdate(self, newTable, tableSource):
        """
        Takes a dict of name:cost and a tableSource thats a name of the neighbor I just got this from
        @newTable:{str:int}
        @tableSource:str
        """
        sendUpdate = False
        for entry in newTable:
            if self.table.checkUpdate(entry, newTable[entry], tableSource):
                sendUpdate = True
        return sendUpdate
    
    def sendMsg(self, to, msgTxt):
        """
        
        """
        msg = {'type': 'message', 'source' : self.myName, 'message' : {'content': msgTxt, 'destination' : to, 'path' : [self.myName]}}
        self.sock.sendto(json.dumps(msg), (to, 50007))
    
    def sendUpdates(self):
        jsonMsg, neighIpDict = self.createOutgoingUpdate()
        for name in neighIpDict:
            self.sock.sendto(jsonMsg, (neighIpDict[name], 50007)) #send a copy of the jsonMsg to each neighbor

    def sendRestart(self):
        jsonMsg, neighIpDict = self.createOutgoingUpdate()
        for name in neighIpDict:
            print("sending restart to %s" % name )
            jsonMsg = {'type':'restart'}
            jsonMsg = json.dumps(jsonMsg).encode('utf8')
            self.sock.sendto(jsonMsg, (neighIpDict[name], 50007)) #send a copy of the jsonMsg to each neighbor
    
    def createOutgoingUpdate(self):
        """
        Return a list of list of a jsonized dict and a list of ips to send to. 
        """
        outDict = {'type': 'table', 'source': self.myName}
        outDict['table'] = self.table.toReport()
        dump = json.dumps(outDict)
        return [dump.encode('utf-8'), self.table.neighbors]
                
    
    def forwardMsg(self, msg):
        """
        Return a list containing an updated jsonized dict with myself added to the list of routers and the next router's ip to send to.
        @msg:str**
        """
        msg['message']['path'].append(self.myName)
        nextIp = self.table.next(msg['message']['destination'])
        if not msg['source']:
            msg['source'] = self.myName
        dump = json.dumps(msg)
        return (dump.encode('utf-8'), nextIp)
            
            
    def amReciever(self, msg):
        """
        Check to see if the receiver of the is myself. Return t/f depending on result.
        @msg:str**
        """
        if msg['message']['destination'] == self.myName:
            return True
        return False
