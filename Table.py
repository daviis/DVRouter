'''
Created on Nov 5, 2014

@author: daviis01
'''
class Table():
    
    def __init__(self):
        self.neighbors = {}
        self.data = {}
        
    def __str__(self):
        st = 'table'
        for name in self.data:
            st += "\t" + name
        st += "\n\t"
        for name in self.data:
            st += '\t' + str(self.data[name][0])
        return st
    
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
        