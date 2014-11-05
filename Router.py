"""
@author:Isaac Davis
@date: 2014-11-05
"""
import sys


class Router:
    
    def __init__(self, aFile):
        try:
            self.table = self._makeInitialTable(aFile)
        except IOError:
            print("File ", aFile, " does not exist", sys.stderr)
            
    def _makeInitialTable(self, aFile):
        someFile = open(aFile, 'r')
        initTable = Table() 
        for line in someFile:
            initTable.addNeighbor(line.split(" "))
        someFile.close()
        return initTable
            
        
class Table():
    
    def __init__(self):
        self.neighbors = {}
        self.data = {}
        
    def addNeighbor(self, name, cost, ip):
        self.neighbors[name] = ip
        self.data[name] = [cost, name]
        
    def updateCost(self, name, cost, neighName):
        totalCost = cost + self.data[neighName][0]
        if self.data[name] > totalCost:
            self.data[name] = [totalCost, neighName]
            return True
        else:
            return False
        
def main():
    router = Router()
    print('made it')
    
if __name__ == "__main__":
    main()