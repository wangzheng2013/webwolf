from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

clients = []
class SimpleEcho(WebSocket):

    def handleMessage(self):
        print self.data
        for client in clients:
            client.sendMessage(self.address[0] + u'-' + self.data)

    def handleConnected(self):
        print self.address, 'connected'
        clients.append(self)

    def handleClose(self):
        print self.address, 'closed'
        clients.remove(self)

server = SimpleWebSocketServer('', 4000, SimpleEcho)
server.serveforever()
