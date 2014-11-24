'''
Created on Nov 5, 2014

@author: daviis01

The internal representation of the data table for the Router class. 
'''
class Table():
    
    def __init__(self):
        """
        Build an empty table with fields initialized to empyt values. Use self.addNeighbor to fill the table. 
        """
        self.neighbors = {} # str:str. name:ip
        self.data = {} #a dict from str:list str is name. List[0] is int of cost. List[1] is the neighbor to send to.
        self.routerName = ""
        
    def __str__(self):
        """
        Printing method for the table
        """
        st = 'table\n'
#        for name in self.data:
#            st += "\t" + name
#        st += "\n"
        for name in self.data:
            st += name + '\t' + str(self.data[name][0]) + ':'+  str(self.data[name][1]) + "\n"
        return st
    
    def addNeighbor(self, name, cost, ip):
        """
        Add a new neighbor to the table. Used for the inital building from start.txt
        
        @name:str
        @cost:int
        @ip:str
        """
        self.neighbors[name] = ip
        self.data[name] = [cost, name]
        
    def addSelf(self, name):
        """
        Help the router figure out what its name is.
        @name:str
        """
        self.routerName = name
        self.data[name] = [0, name]
        
    def checkUpdate(self, name, cost, neighName):
        """
        @name:str
        @cost:int
        @nighName:str
        """
        totalCost = cost + self.data[neighName][0]
        if name in self.data:
            if self.data[name][0] > totalCost:
                self.data[name] = [totalCost, neighName]
                return True
            else:
                return False
        else:
            self.data[name] = [totalCost, neighName]
            return True
        
    def next(self, dest):
        """
        The name of the person the message is destined for comes in. The neighbor's ip to forward it to is returned. 
        @dest:str 
        """
        route = self.data[dest][1]
        return self.neighbors[route]
        
    def toReport(self):
        """
        A printing method for easier reading.
        """
        repDict = {}
        for key in self.data:
            if key != self.routerName:
                repDict[key] = self.data[key][0]
        return repDict
        
