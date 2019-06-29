import time
import hashlib
import socket  # Import socket module
import threading
import sys
from itertools import chain, product

import time


def brute_force(charset, maxlength):
    return (''.join(candidate)
            for candidate in chain.from_iterable(product(charset, repeat=i)
                                                 for i in range(1, maxlength + 1)))


def get_sha1(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()

class Slave:
    def __init__(self, host, port):
        self.slave_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.slave_socket.settimeout(41.0)

        self.limit=3
        self.hard=5
        
        self.addr=(host,int(port))

        self.tasks = []
        self.task = ""
        self.to_break = ""

        threading.Thread(target=self.conn).start()
        threading.Thread(target=self.work).start()

    def handlejob(self,data):
        if data[0] == "job":
            self.tasks.append((data[1],data[2]))
            print("Job accepted {} {}".format(data[1],data[2]))
        else:
            print("Job rejected {}".format(str(data)))

    def send_res(self,res):
        print("Sending result [{}]".format(res))
        self.slave_socket.sendto(("res:"+res).encode(),self.addr)

    def send_r(self):
        if len(self.tasks)<3:
            print("Sending job request")
            self.slave_socket.sendto(b'job',self.addr)

    def conn(self):
        while True:
            try:
                self.send_r()
                data, server = self.slave_socket.recvfrom(1024)
                data =  data.decode().split(":")
                self.handlejob(data)
                time.sleep(2)
            except socket.timeout:
                pass
   
    def work(self):
        while True:
            if len(self.tasks):
                d=self.tasks.pop()
                self.to_break=d[0]
                self.task=d[1]
                res=self.break_code()
                res=res.split(":")
                if res[0]=="pass":
                    self.send_res(res[2])
                    self.tasks=[]
            #print("working")

    def break_code(self, length=1):
        """
        just a tool of slave
        """
        #print("/ breaking {} with {}".format(self.to_break,self.task))
        print("/ ")
        time.sleep(self.hard)
        for guess in brute_force(self.task, length):
            if get_sha1(guess) == self.to_break:
                return "pass:" + self.to_break + ':' + guess
        if length > self.limit:
            # print("LENGTH LIMIT REACHED {}".format(length))
            return "fail"
        else:
            return self.break_code(length + 1)

if __name__ == '__main__':
    Slave(sys.argv[1], int(sys.argv[2]))

