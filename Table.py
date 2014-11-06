'''
Created on Nov 5, 2014

@author: daviis01
'''
class Table():
    
    def __init__(self):
        self.neighbors = {}
        self.data = {}
        
    def addNeighbor(self, name, cost, ip):
        self.neighbors[name] = ip
        self.data[name] = [cost, name]
        
    def checkUpdate(self, name, cost, neighName):
        totalCost = cost + self.data[neighName][0]
        if self.data[name] > totalCost:
            self.data[name] = [totalCost, neighName]
            return True
        else:
            return False
        
    def toReport(self):
        return self.data
        