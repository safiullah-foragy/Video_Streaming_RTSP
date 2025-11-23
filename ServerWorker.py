"""
RTSP Server Worker Thread
Handles individual client connections and RTSP protocol
"""

import sys
import traceback
import threading
import socket
from random import randint
from time import sleep

from RtpPacket import RtpPacket
from VideoStream import VideoStream
import config


class ServerWorker:
    """Worker thread to handle one RTSP client connection"""
    
    SETUP = config.SETUP
    PLAY = config.PLAY
    PAUSE = config.PAUSE
    TEARDOWN = config.TEARDOWN
    
    INIT = config.INIT
    READY = config.READY
    PLAYING = config.PLAYING
    
    state = INIT
    
    OK_200 = 0
    FILE_NOT_FOUND_404 = 1
    CON_ERR_500 = 2
    
    clientInfo = {}
    
    def __init__(self, clientInfo):
        """Initialize worker with client connection info"""
        self.clientInfo = clientInfo
        
    def run(self):
        """Main loop to receive and handle RTSP requests"""
        threadName = threading.current_thread().name
        print(f'[{threadName}] Connection from: {self.clientInfo["addr"]}')
        
        self.clientInfo['socket'].settimeout(30)  # 30 second timeout
        
        while True:
            try:
                data = self.clientInfo['socket'].recv(256)
                if data:
                    print(f'[{threadName}] Received from client: {data.decode("utf-8")}')
                    self.processRtspRequest(data.decode("utf-8"))
                else:
                    break
            except socket.timeout:
                print(f'[{threadName}] Client timeout')
                break
            except Exception as e:
                print(f'[{threadName}] Error: {e}')
                break
        
        # Clean up
        if self.clientInfo['session'] in self.clientInfo:
            if 'videoStream' in self.clientInfo:
                self.clientInfo['videoStream'].close()
        
        print(f'[{threadName}] Connection closed')
    
    def processRtspRequest(self, data):
        """Parse and handle RTSP request"""
        request = data.split('\n')
        line1 = request[0].split(' ')
        requestType = line1[0]
        
        # Get the RTSP sequence number
        seqNum = request[1].split(' ')[1]
        
        # Handle different request types
        if requestType == self.SETUP:
            if self.state == self.INIT:
                print('[RTSP] Processing SETUP')
                
                try:
                    # Get filename from request
                    filename = line1[1]
                    
                    # Open video stream
                    self.clientInfo['videoStream'] = VideoStream(filename)
                    
                    # Generate session ID
                    self.clientInfo['session'] = randint(100000, 999999)
                    
                    # Send RTSP reply
                    self.replyRtsp(self.OK_200, seqNum)
                    
                    # Get RTP port from request
                    for line in request:
                        if line.startswith('Transport:'):
                            # Extract client_port
                            parts = line.split(';')
                            for part in parts:
                                if 'client_port' in part:
                                    self.clientInfo['rtpPort'] = int(part.split('=')[1].split('-')[0])
                    
                    # Update state
                    self.state = self.READY
                    print(f'[RTSP] State changed to READY. Session: {self.clientInfo["session"]}')
                    
                except IOError:
                    print('[RTSP] Error: Video file not found')
                    self.replyRtsp(self.FILE_NOT_FOUND_404, seqNum)
        
        elif requestType == self.PLAY:
            if self.state == self.READY:
                print('[RTSP] Processing PLAY')
                
                self.state = self.PLAYING
                
                # Create RTP socket
                self.clientInfo['rtpSocket'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Send RTSP reply
                self.replyRtsp(self.OK_200, seqNum)
                
                # Start sending video frames
                self.clientInfo['event'] = threading.Event()
                self.clientInfo['worker'] = threading.Thread(target=self.sendRtp)
                self.clientInfo['worker'].start()
                print(f'[RTSP] State changed to PLAYING')
        
        elif requestType == self.PAUSE:
            if self.state == self.PLAYING:
                print('[RTSP] Processing PAUSE')
                
                self.state = self.READY
                
                # Stop the RTP streaming thread
                self.clientInfo['event'].set()
                
                # Send RTSP reply
                self.replyRtsp(self.OK_200, seqNum)
                print(f'[RTSP] State changed to READY')
        
        elif requestType == self.TEARDOWN:
            print('[RTSP] Processing TEARDOWN')
            
            # Stop streaming if playing
            if self.state == self.PLAYING:
                self.clientInfo['event'].set()
            
            # Send RTSP reply
            self.replyRtsp(self.OK_200, seqNum)
            
            # Close sockets
            if 'rtpSocket' in self.clientInfo:
                self.clientInfo['rtpSocket'].close()
            
            # Close video stream
            if 'videoStream' in self.clientInfo:
                self.clientInfo['videoStream'].close()
    
    def sendRtp(self):
        """Send video frames via RTP"""
        print('[RTP] Starting video stream')
        
        while True:
            # Check if stopped
            if self.clientInfo['event'].is_set():
                break
            
            # Get next frame
            data = self.clientInfo['videoStream'].nextFrame()
            
            if data:
                frameNumber = self.clientInfo['videoStream'].frameNbr()
                
                try:
                    # Create RTP packet
                    packet = RtpPacket()
                    packet.encode(2, 0, 0, 0, frameNumber, 0, 26, 0, data)
                    
                    # Send packet
                    self.clientInfo['rtpSocket'].sendto(
                        packet.getPacket(),
                        (self.clientInfo['addr'][0], self.clientInfo['rtpPort'])
                    )
                    
                    print(f'[RTP] Sent frame #{frameNumber}')
                    
                except Exception as e:
                    print(f'[RTP] Error sending frame: {e}')
            else:
                # End of video, reset for loop
                self.clientInfo['videoStream'].reset()
                print('[RTP] End of video, restarting...')
            
            # Frame rate control (24 fps = ~42ms per frame)
            sleep(1.0 / config.FRAME_RATE)
        
        print('[RTP] Stopped video stream')
    
    def replyRtsp(self, code, seq):
        """Send RTSP reply to client"""
        if code == self.OK_200:
            reply = f'{config.RTSP_VER} 200 OK\n'
            reply += f'CSeq: {seq}\n'
            if self.state == self.READY:
                reply += f'Session: {self.clientInfo["session"]}\n'
        elif code == self.FILE_NOT_FOUND_404:
            reply = f'{config.RTSP_VER} 404 NOT FOUND\n'
            reply += f'CSeq: {seq}\n'
        elif code == self.CON_ERR_500:
            reply = f'{config.RTSP_VER} 500 CONNECTION ERROR\n'
            reply += f'CSeq: {seq}\n'
        
        try:
            self.clientInfo['socket'].send(reply.encode())
            print(f'[RTSP] Sent reply:\n{reply}')
        except Exception as e:
            print(f'[RTSP] Error sending reply: {e}')
