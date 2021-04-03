from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Server(DatagramProtocol):
    def __init__(self) :
        print('Running the server ...')
        self.clients = set()

    def send_message_loop(self, connectedClients, addr, userDetails):
        
        for host, port, username in self.clients:
            address = ( host, port )
            self.transport.write(connectedClients.encode('utf-8'), address)
        
        print(f"Connected clients : {len(self.clients)}")
    
    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')
        if datagram:
            userDetails = (addr[0], addr[1], datagram)
            self.clients.add(userDetails)
            connectedClients = ""
            for host, port, username in self.clients:
                connectedClients += f"{host}|{port}|{username}|"
            
            self.send_message_loop(connectedClients, addr, userDetails)
            

if __name__ == "__main__":
    port = 9999
    reactor.listenUDP(port, Server())
    reactor.run()
    

