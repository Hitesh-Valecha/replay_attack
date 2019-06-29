import threading, sys
import random, string
import socket

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


class BreakRoom:
    def __init__(self, host, port, code):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host,port))
        
        self.code=code
        self.the_queue = []
        self._generate_new_queue()

        threading.Thread(name="comm", target=self.comm).start()


    def gettask(self):
        if not len(self.the_queue):
            return b'Thanks no work rn'
        job=self.the_queue.pop()
        print("Sending job "+job)
        return "job"+":"+self.code+":"+job

    def comm(self):
        while True:
            m, address = self.server_socket.recvfrom(1024)
            #print("What"+str(message)+"   "+str(address))
            m=decrypt(m.decode())
            m=m.split(":")
            if m[0] == 'job':
                self.crsend(self.gettask(),address)
                print(address)
            elif m[0] == 'res':
                print("GOT RESULT : {}".format(m[1]))
                break
            elif m[0] == 'auth':
                #handle auth right here
                self.crsend("auth:"+decrypt(m[1]),address)
        
    def crsend(self,data,server):
        en=encrypt(data)
        self.server_socket.sendto(en.encode(),server)
    
    def _generate_new_queue(self):
        nums = '1234567890'
        special = '`~!@#$%^&*()_+-='
        space = ' '
        self.the_queue.append(str(string.ascii_lowercase))
        self.the_queue.append(str(string.ascii_letters))
        self.the_queue.append(str(string.ascii_lowercase + nums))
        self.the_queue.append(str(string.ascii_letters + nums))
        self.the_queue.append(str(string.ascii_uppercase))
        self.the_queue.append(str(string.ascii_uppercase + nums))
        self.the_queue.append(str(string.ascii_lowercase + nums + special))
        self.the_queue.append(str(string.ascii_lowercase + special))
        self.the_queue.append(str(string.ascii_letters + special))
        self.the_queue.append(str(string.ascii_letters + nums + special))
        self.the_queue.append(str(string.ascii_uppercase + nums + special))
        self.the_queue.append(str(string.ascii_uppercase + special))
        self.the_queue.append(str(string.ascii_lowercase + nums + space))
        self.the_queue.append(str(string.ascii_uppercase + nums + space))
        self.the_queue.append(str(string.ascii_letters + nums + space))
        self.the_queue.append(str(string.ascii_lowercase + nums + space))
        self.the_queue.append(str(string.ascii_uppercase + nums + space))
        self.the_queue.append(str(string.ascii_letters + nums + space))
        self.the_queue.reverse()



if __name__ == '__main__':
    if len(sys.argv) == 4:
        BreakRoom(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        print("syntax : python3 master.py [local ip addr] [port] [sha1 code /sha1 file] optional[no of localslaves]\n "
              "eg     : python3 master.py 192.168.1.105 9987 e5acb1a96e34cd7f263aada0b69aa58bdd722a03 3 ")
