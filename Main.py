'''
Created on Nov 5, 2014

@author: daviis01

Set up the Router, Table and a communal queue. The start file gets configured here. Also used for user interaction to push messages onto the queue and 
issue table dumps and soft restarts.
'''
import Router, SockReader
import queue
import json


def main():
    q = queue.Queue()
    
    router = Router.Router("/Users/sysadmin/school/cs341/dvRouter/DVRouter/start.txt", q)
    sockReader = SockReader.SockReader(q)
    
    sockReader.start()
    router.start()
    
    while True:
        print()
        to = input("to->")
        msg = input("msg->")
        aDict = {}
        if not to and not msg:
            continue
        if to == '$table':
            aDict = {'type': 'printTable'}
        elif to == 'restart':
            aDict = {'type': 'restart'}
        else:
            aDict = {'type': 'message', 'message' : {'content': msg, 'destination' : to, 'path' : []}, 'source' : None}
        msg = json.dumps(aDict)
        q.put(msg.encode('utf-8'))
        
        
    
if __name__ == "__main__":
    main()