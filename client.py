from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint

class Client(DatagramProtocol):
    def __init__(self, host, port):
        if host == 'localhost':
            host = '127.0.0.1'
        
        self.username = input('Username : ')
        self.id = ( host, port )
        self.addr = None
        self.server = ('127.0.0.1', 9999)
        self.sendTo = None
        print(f'IP : {host}')
        print(f'Port : {port}')
    
    def startProtocol(self):
        self.transport.write(self.username.encode('utf-8'), self.server)

    def getHostPort(self, datagram, username):
        addr = None
        for data in datagram:
            if data[-1] == username:
                addr =  (data[0], int(data[1]))
                break
        return addr

    def show(self, datagram):
        print("  Online  ".center(60,"="))
        for data in datagram:
            print(data[-1].center(60," "))
        print("=".center(60, "="))

    def checkUsername(self, datagram):
        newDatagram = []
        for data in datagram:
            if data[-1] == self.username:
                pass
            else:
                newDatagram.append(data)
        
        return newDatagram
    
    def toListTuple(self, datagram):
        result = []
        tup = []

        for i,data in enumerate(datagram):
            i = i + 1
            tup.append(data)
            if i % 3 == 0:
                result.append(tup)
                tup = []
        
        return result
    
    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')
        if addr == self.server:
            datagram = datagram.split('|')
            datagram = self.toListTuple(datagram)
            datagram = self.checkUsername(datagram)
            self.show(datagram)
            if datagram != []:
                self.sendTo = input('Choose a Client : ')
                self.addr = self.getHostPort(datagram, self.sendTo)
                while self.addr is None:
                    print('Someone like that doesnt exist ...')
                    self.sendTo = input('Choose a Client : ')
                    self.addr = self.getHostPort(datagram, self.sendTo)

                reactor.callInThread(self.send_message)
        else:
            print('\n',f"{self.sendTo} : {datagram}")
    
    def send_message(self):
        while True:
            self.transport.write(input('==> ').encode('utf-8'), self.addr)
    

if __name__ == "__main__":
    try:
        port = randint(1000,9998)
        reactor.listenUDP(port, Client('127.0.0.1', port))
        reactor.run()
    except:
        print(f'PORT : {port} is busy ...')
        print('Looking for a new port ...')
        port = randint(1000,9998)
        reactor.listenUDP(port, Client('127.0.0.1', port))
        reactor.run()
    