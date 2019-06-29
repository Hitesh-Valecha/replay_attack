import time, random
import hashlib
import socket  # Import socket module
import threading
import sys
from itertools import chain, product

import time

#p=21 q=109 n=2289 e=7 d=1543
def encrypt(data):
    e,n=7,2289
    #print("encrypting : "+data)
    intdata = [x for x in map(ord, data)]
    crypteddata = [((x ** e) % n) for x in intdata]
    return ",".join(map(str, crypteddata))

def decrypt(data):
    d,n=1543,2289
    #print("decrypting : "+data)
    decrypteddata = [(x ** d) % n for x in map(int,data.split(','))]
    decryptedchar = [x for x in map(chr, decrypteddata)]
    return "".join(map(str, decryptedchar))


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

        self.rand=0
        self.data=0

        self.trusted=[]

        self.tasks = []
        self.task = ""
        self.to_break = ""

        threading.Thread(target=self.conn).start()
        threading.Thread(target=self.work).start()
    
    def crsend(self,data,server):
        en=encrypt(data)
        self.slave_socket.sendto(en.encode(),server)

    def challenge(self,server):
        print("Challenging "+ str(server))
        self.rand = random.randint(1,1000)
        self.crsend("auth:"+str(encrypt(str(self.rand))),server)
    
    def authenticate(self,auth,server):
        if int(auth) == self.rand:
            self.rand=0
            print("Server authenticated : "+str(server))
            self.trusted.append(server)
            self.handlejob(self.data,server)


    def handlejob(self,data,server):
        if data[0] == "auth":
            self.authenticate(data[1],server)
        if server in self.trusted:
            if data[0] == "job":
                self.tasks.append((data[1],data[2]))
                print("Job accepted {} {}".format(data[1],data[2]))
        else:
            print("Job rejected {}".format(str(data)))
            self.challenge(server)
            self.data=data

    def send_res(self,res):
        print("Sending result [{}]".format(res))
        self.crsend("res:"+res,self.addr)

    def send_r(self):
        if len(self.tasks)<3:
            print("Sending job request")
            self.crsend('job',self.addr)

    def conn(self):
        while True:
            try:
                self.send_r()
                data, server = self.slave_socket.recvfrom(1024)
                data = decrypt(data.decode())
                data =  data.split(":")
                self.handlejob(data,server)
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

