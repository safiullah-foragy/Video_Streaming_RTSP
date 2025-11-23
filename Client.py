"""
RTSP Client with YouTube-like GUI
Provides a modern interface for video streaming with RTSP/RTP protocols
"""

import sys
import socket
import threading
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import io
import time

from RtpPacket import RtpPacket
import config


class Client:
    """RTSP Client with GUI"""
    
    # RTSP states
    INIT = 0
    READY = 1
    PLAYING = 2
    
    # RTSP commands
    SETUP = 'SETUP'
    PLAY = 'PLAY'
    PAUSE = 'PAUSE'
    TEARDOWN = 'TEARDOWN'
    
    def __init__(self, master, serveraddr, serverport, rtpport, filename):
        """Initialize client with GUI"""
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handler)
        self.master.title("Video Streaming - YouTube Style")
        self.master.geometry("900x700")
        self.master.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Server info
        self.serverAddr = serveraddr
        self.serverPort = int(serverport)
        self.rtpPort = int(rtpport)
        self.fileName = filename
        self.rtspSeq = 0
        self.sessionId = 0
        self.requestSent = -1
        self.teardownAcked = 0
        self.state = self.INIT
        self.frameNbr = 0
        self.rtpSocket = None
        self.rtspSocket = None
        
        # Statistics
        self.totalBytes = 0
        self.totalFrames = 0
        self.startTime = 0
        self.lastFrameTime = 0
        
        # Create GUI
        self.createWidgets()
        
    def createWidgets(self):
        """Create all GUI widgets"""
        # Set background color
        self.master.configure(bg='#181818')
        
        # ===== TOP FRAME - Title =====
        topFrame = Frame(self.master, bg='#212121', height=60)
        topFrame.pack(side=TOP, fill=X, padx=0, pady=0)
        topFrame.pack_propagate(False)
        
        titleLabel = Label(topFrame, text="🎬 Video Streaming Player", 
                          font=('Helvetica', 18, 'bold'), 
                          fg='white', bg='#212121')
        titleLabel.pack(pady=15)
        
        # ===== MIDDLE FRAME - Video Display =====
        videoFrame = Frame(self.master, bg='#000000', relief=SUNKEN, bd=2)
        videoFrame.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=10)
        
        # Video label with placeholder
        self.label = Label(videoFrame, bg='#000000')
        self.label.pack(fill=BOTH, expand=True)
        
        # Show placeholder
        self.showPlaceholder()
        
        # ===== PROGRESS BAR =====
        progressFrame = Frame(self.master, bg='#181818')
        progressFrame.pack(side=TOP, fill=X, padx=20, pady=(0, 10))
        
        self.progressBar = ttk.Scale(progressFrame, from_=0, to=100, 
                                     orient=HORIZONTAL, command=self.onProgressChange)
        self.progressBar.pack(fill=X)
        self.progressBar.set(0)
        
        # ===== CONTROL PANEL =====
        controlFrame = Frame(self.master, bg='#282828', height=120)
        controlFrame.pack(side=TOP, fill=X, padx=20, pady=(0, 10))
        controlFrame.pack_propagate(False)
        
        # Buttons container
        buttonContainer = Frame(controlFrame, bg='#282828')
        buttonContainer.pack(pady=15)
        
        # Style for buttons
        btnStyle = {
            'font': ('Helvetica', 11, 'bold'),
            'width': 12,
            'height': 2,
            'relief': RAISED,
            'bd': 2,
            'cursor': 'hand2'
        }
        
        # Setup button
        self.setup = Button(buttonContainer, text="⚙ SETUP", 
                           command=self.setupMovie, 
                           bg='#3ea6ff', fg='white', 
                           activebackground='#2690e8',
                           **btnStyle)
        self.setup.grid(row=0, column=0, padx=5)
        
        # Play button
        self.start = Button(buttonContainer, text="▶ PLAY", 
                           command=self.playMovie, 
                           bg='#ff0000', fg='white',
                           activebackground='#cc0000',
                           state=DISABLED, **btnStyle)
        self.start.grid(row=0, column=1, padx=5)
        
        # Pause button
        self.pause = Button(buttonContainer, text="⏸ PAUSE", 
                           command=self.pauseMovie, 
                           bg='#909090', fg='white',
                           activebackground='#707070',
                           state=DISABLED, **btnStyle)
        self.pause.grid(row=0, column=2, padx=5)
        
        # Stop button
        self.teardown = Button(buttonContainer, text="⏹ STOP", 
                              command=self.exitClient, 
                              bg='#606060', fg='white',
                              activebackground='#404040',
                              state=DISABLED, **btnStyle)
        self.teardown.grid(row=0, column=3, padx=5)
        
        # ===== STATUS BAR =====
        statusFrame = Frame(self.master, bg='#212121', height=50)
        statusFrame.pack(side=BOTTOM, fill=X)
        statusFrame.pack_propagate(False)
        
        # Status info
        infoContainer = Frame(statusFrame, bg='#212121')
        infoContainer.pack(pady=8)
        
        self.statusLabel = Label(infoContainer, 
                                text="Status: Not Connected", 
                                font=('Helvetica', 9), 
                                fg='#aaaaaa', bg='#212121')
        self.statusLabel.grid(row=0, column=0, padx=20)
        
        self.frameLabel = Label(infoContainer, 
                               text="Frame: 0", 
                               font=('Helvetica', 9), 
                               fg='#aaaaaa', bg='#212121')
        self.frameLabel.grid(row=0, column=1, padx=20)
        
        self.bitrateLabel = Label(infoContainer, 
                                 text="Bitrate: 0 kbps", 
                                 font=('Helvetica', 9), 
                                 fg='#aaaaaa', bg='#212121')
        self.bitrateLabel.grid(row=0, column=2, padx=20)
        
        self.fpsLabel = Label(infoContainer, 
                             text="FPS: 0", 
                             font=('Helvetica', 9), 
                             fg='#aaaaaa', bg='#212121')
        self.fpsLabel.grid(row=0, column=3, padx=20)
    
    def showPlaceholder(self):
        """Show placeholder when no video is playing"""
        # Create a simple placeholder image
        placeholder = Image.new('RGB', (640, 480), color='#1a1a1a')
        photo = ImageTk.PhotoImage(placeholder)
        self.label.configure(image=photo)
        self.label.image = photo
        
        # Add text overlay would require PIL drawing, keeping it simple
    
    def onProgressChange(self, value):
        """Handle progress bar changes"""
        # This would be used for seeking (not implemented in basic version)
        pass
    
    def setupMovie(self):
        """Send SETUP request"""
        if self.state == self.INIT:
            self.sendRtspRequest(self.SETUP)
            self.updateStatus("Connecting to server...")
    
    def exitClient(self):
        """Send TEARDOWN request and exit"""
        self.sendRtspRequest(self.TEARDOWN)
        self.updateStatus("Disconnecting...")
        self.master.after(500, self.master.destroy)
    
    def pauseMovie(self):
        """Send PAUSE request"""
        if self.state == self.PLAYING:
            self.sendRtspRequest(self.PAUSE)
            self.updateStatus("Paused")
    
    def playMovie(self):
        """Send PLAY request"""
        if self.state == self.READY:
            # Create RTP socket
            threading.Thread(target=self.listenRtp, daemon=True).start()
            self.sendRtspRequest(self.PLAY)
            self.startTime = time.time()
            self.updateStatus("Playing...")
    
    def listenRtp(self):
        """Listen for RTP packets"""
        while True:
            try:
                if self.state == self.PLAYING:
                    data = self.rtpSocket.recv(config.MAX_PACKET_SIZE)
                    if data:
                        rtpPacket = RtpPacket()
                        rtpPacket.decode(data)
                        
                        currFrameNbr = rtpPacket.seqNum()
                        
                        if currFrameNbr > self.frameNbr:
                            self.frameNbr = currFrameNbr
                            self.updateMovie(rtpPacket.getPayload())
                            self.updateStatistics(len(data))
                else:
                    time.sleep(0.1)
            except:
                if self.teardownAcked == 1:
                    break
    
    def updateMovie(self, imageData):
        """Update the video display"""
        try:
            image = Image.open(io.BytesIO(imageData))
            
            # Resize to fit display
            display_width = 640
            display_height = 480
            image = image.resize((display_width, display_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            self.label.configure(image=photo)
            self.label.image = photo
            
            # Update frame counter
            self.frameLabel.config(text=f"Frame: {self.frameNbr}")
            
        except Exception as e:
            print(f"Error updating frame: {e}")
    
    def updateStatistics(self, packetSize):
        """Update streaming statistics"""
        self.totalBytes += packetSize
        self.totalFrames += 1
        
        currentTime = time.time()
        elapsedTime = currentTime - self.startTime
        
        if elapsedTime > 0:
            # Calculate bitrate in kbps
            bitrate = (self.totalBytes * 8) / (elapsedTime * 1000)
            self.bitrateLabel.config(text=f"Bitrate: {bitrate:.1f} kbps")
            
            # Calculate FPS
            fps = self.totalFrames / elapsedTime
            self.fpsLabel.config(text=f"FPS: {fps:.1f}")
        
        self.lastFrameTime = currentTime
    
    def updateStatus(self, message):
        """Update status label"""
        self.statusLabel.config(text=f"Status: {message}")
    
    def connectToServer(self):
        """Connect to RTSP server"""
        try:
            self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.rtspSocket.connect((self.serverAddr, self.serverPort))
            print(f"Connected to {self.serverAddr}:{self.serverPort}")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to server:\n{e}")
    
    def sendRtspRequest(self, requestCode):
        """Send RTSP request to server"""
        # Setup connection if not connected
        if requestCode == self.SETUP and self.rtspSocket is None:
            self.connectToServer()
        
        # Increment sequence number
        self.rtspSeq += 1
        
        # Build request
        request = f"{requestCode} {self.fileName} {config.RTSP_VER}\n"
        request += f"CSeq: {self.rtspSeq}\n"
        
        if requestCode == self.SETUP:
            # Create RTP socket for receiving
            self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.rtpSocket.settimeout(0.5)
            
            # Bind to RTP port
            try:
                self.rtpSocket.bind(('', self.rtpPort))
            except:
                messagebox.showerror("Socket Error", 
                                   f"Unable to bind to port {self.rtpPort}")
                return
            
            request += f"Transport: RTP/UDP; client_port= {self.rtpPort}\n"
        else:
            request += f"Session: {self.sessionId}\n"
        
        # Send request
        try:
            self.rtspSocket.send(request.encode())
            print(f"\nSent RTSP request:\n{request}")
            
            # Store request type
            self.requestSent = requestCode
            
            # Wait for response
            self.recvRtspReply()
            
        except Exception as e:
            print(f"Error sending request: {e}")
            messagebox.showerror("Error", f"Failed to send request:\n{e}")
    
    def recvRtspReply(self):
        """Receive RTSP reply from server"""
        try:
            data = self.rtspSocket.recv(1024)
            if data:
                reply = data.decode("utf-8")
                print(f"Received RTSP reply:\n{reply}")
                
                # Parse reply
                lines = reply.split('\n')
                seqNum = int(lines[1].split(' ')[1])
                
                # Check if request matches reply
                if seqNum == self.rtspSeq:
                    statusLine = lines[0].split(' ')
                    statusCode = int(statusLine[1])
                    
                    if statusCode == 200:
                        # Process based on request type
                        if self.requestSent == self.SETUP:
                            # Get session ID
                            self.sessionId = int(lines[2].split(' ')[1])
                            self.state = self.READY
                            
                            # Enable buttons
                            self.start.config(state=NORMAL)
                            self.teardown.config(state=NORMAL)
                            self.setup.config(state=DISABLED)
                            
                            self.updateStatus("Ready")
                            
                        elif self.requestSent == self.PLAY:
                            self.state = self.PLAYING
                            self.pause.config(state=NORMAL)
                            self.start.config(state=DISABLED)
                            
                        elif self.requestSent == self.PAUSE:
                            self.state = self.READY
                            self.start.config(state=NORMAL)
                            self.pause.config(state=DISABLED)
                            
                        elif self.requestSent == self.TEARDOWN:
                            self.state = self.INIT
                            self.teardownAcked = 1
                    else:
                        print(f"Error: Server returned status {statusCode}")
                        
        except Exception as e:
            print(f"Error receiving reply: {e}")
    
    def handler(self):
        """Handle window close event"""
        if self.state != self.INIT:
            self.sendRtspRequest(self.TEARDOWN)
            if self.rtpSocket:
                self.rtpSocket.close()
            if self.rtspSocket:
                self.rtspSocket.close()
        
        self.master.destroy()


def main():
    """Main entry point"""
    try:
        # Default parameters
        serverAddr = config.SERVER_HOST
        serverPort = config.RTSP_PORT
        rtpPort = config.RTP_PORT
        fileName = config.VIDEO_FILE
        
        # Allow command line arguments
        if len(sys.argv) > 1:
            serverAddr = sys.argv[1]
        if len(sys.argv) > 2:
            serverPort = sys.argv[2]
        if len(sys.argv) > 3:
            rtpPort = sys.argv[3]
        if len(sys.argv) > 4:
            fileName = sys.argv[4]
        
        # Create GUI
        root = Tk()
        app = Client(root, serverAddr, serverPort, rtpPort, fileName)
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting client: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
