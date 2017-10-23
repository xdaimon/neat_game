import sys
import json
from Game import Game
import Test

if (sys.version_info > (3, 0)):
    print("Python 3.X detected")
    import socketserver as ss
else:
    print("Python 2.X detected")
    import SocketServer as ss

class NetworkHandler(ss.StreamRequestHandler):
    def get_msg(self):
        # reads until '\n' encountered
        return json.loads(str(self.rfile.readline().decode()))

    def send_msg(self, response):
        self.wfile.write((json.dumps(response, separators=(',', ':')) + '\n').encode())

    def handle(self):
        game = Game()
        while True:
            game.parse_msg(self.get_msg())
            response = game.get_cmd()
            if response:
                self.send_msg(response)
            else:
                print('Response Empty or None!')
                exit(-1)


# TODO Tell Game() that it should use an agent with a certain strategy. For
# testing purposes.
def main():
    if 'test' in sys.argv:
        Test.test()
        return

    host = '127.0.0.1'
    port = int(len(sys.argv)>1 and sys.argv[1]) or 9090
    try:
        server = ss.TCPServer((host, port), NetworkHandler)
    except OSError:
        port += 1
        server = ss.TCPServer((host, port), NetworkHandler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()


if __name__ == "__main__":
    main()
