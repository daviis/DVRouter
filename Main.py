'''
Created on Nov 5, 2014

@author: daviis01
'''
import Router, SockReader
import queue


def main():
    q = queue.Queue()
    
    router = Router.Router("/Users/sysadmin/school/cs341/dvRouter/DVRouter/neighbor.txt", q, "Isaac")
    sockReader = SockReader.SockReader(q)
    
    sockReader.start()
    router.start()
    
if __name__ == "__main__":
    main()