'''
Created on Nov 5, 2014

@author: daviis01
'''
import Router, SockReader
import queue


def main():
    q = queue.Queue()
    
    router = Router.Router("/Users/sysadmin/school/cs341/dvRouter/DVRouter/start.txt", q)
    sockReader = SockReader.SockReader(q)
    
    sockReader.start()
    router.start()
    
#     while True:
#         to = input("to->")
#         msg = input("msg->")
        
    
if __name__ == "__main__":
    main()