import socket, sys

if __name__ == '__main__':
    ss=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr=(sys.argv[1],int(sys.argv[2]))
    for _ in range(int(sys.argv[4])):
            ss.sendto(sys.argv[3].encode(),addr)
