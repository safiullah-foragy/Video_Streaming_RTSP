"""
RTSP Server
Main server that listens for client connections and spawns worker threads
"""

import sys
import socket
import threading

from ServerWorker import ServerWorker
import config


class Server:
    """Main RTSP server class"""
    
    def __init__(self):
        """Initialize server"""
        self.host = config.SERVER_HOST
        self.port = config.RTSP_PORT
        self.socket = None
        
    def start(self):
        """Start the RTSP server"""
        print(f'[SERVER] Starting RTSP server on {self.host}:{self.port}')
        
        # Create TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Bind and listen
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f'[SERVER] RTSP server ready. Waiting for connections...')
            
            # Accept client connections
            while True:
                clientSocket, addr = self.socket.accept()
                
                # Create worker for this client
                clientInfo = {
                    'socket': clientSocket,
                    'addr': addr,
                    'rtpPort': 0,
                    'session': 0
                }
                
                # Start worker thread
                worker = ServerWorker(clientInfo)
                thread = threading.Thread(target=worker.run, name=f'Client-{addr[0]}:{addr[1]}')
                thread.daemon = True
                thread.start()
                
        except KeyboardInterrupt:
            print('\n[SERVER] Server interrupted by user')
        except Exception as e:
            print(f'[SERVER] Error: {e}')
        finally:
            print('[SERVER] Shutting down server...')
            if self.socket:
                self.socket.close()


def main():
    """Main entry point"""
    server = Server()
    server.start()


if __name__ == '__main__':
    main()
