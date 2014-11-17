'''
Created on Nov 5, 2014

@author: daviis01
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
        else:
            aDict = {'type': 'message', 'message' : {'content': msg, 'destination' : to, 'path' : []}, 'source' : None}
        msg = json.dumps(aDict)
        q.put(msg.encode('utf-8'))
        
        
    
if __name__ == "__main__":
    main()