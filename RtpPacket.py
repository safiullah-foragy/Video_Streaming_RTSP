"""
RTP Packet Handler
Handles the creation and parsing of RTP packets for video streaming
"""

import sys
from time import time

HEADER_SIZE = 12


class RtpPacket:
    """Class to handle RTP packet creation and parsing"""
    
    header = bytearray(HEADER_SIZE)
    
    def __init__(self):
        pass
    
    def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
        """
        Encode the RTP packet with header + payload
        
        Args:
            version: RTP version (2 bits)
            padding: Padding flag (1 bit)
            extension: Extension flag (1 bit)
            cc: CSRC count (4 bits)
            seqnum: Sequence number (16 bits)
            marker: Marker bit (1 bit)
            pt: Payload type (7 bits) - 26 for JPEG
            ssrc: Synchronization source identifier (32 bits)
            payload: The actual payload data
        """
        timestamp = int(time())
        
        # Fill the header bytearray with RTP header fields
        # Byte 0: V(2), P(1), X(1), CC(4)
        self.header[0] = (version << 6) | (padding << 5) | (extension << 4) | cc
        
        # Byte 1: M(1), PT(7)
        self.header[1] = (marker << 7) | pt
        
        # Bytes 2-3: Sequence number
        self.header[2] = (seqnum >> 8) & 0xFF
        self.header[3] = seqnum & 0xFF
        
        # Bytes 4-7: Timestamp
        self.header[4] = (timestamp >> 24) & 0xFF
        self.header[5] = (timestamp >> 16) & 0xFF
        self.header[6] = (timestamp >> 8) & 0xFF
        self.header[7] = timestamp & 0xFF
        
        # Bytes 8-11: SSRC
        self.header[8] = (ssrc >> 24) & 0xFF
        self.header[9] = (ssrc >> 16) & 0xFF
        self.header[10] = (ssrc >> 8) & 0xFF
        self.header[11] = ssrc & 0xFF
        
        # Get the payload from the argument
        self.payload = payload
    
    def decode(self, byteStream):
        """
        Decode the RTP packet
        
        Args:
            byteStream: The received packet as bytes
        """
        self.header = bytearray(byteStream[:HEADER_SIZE])
        self.payload = byteStream[HEADER_SIZE:]
    
    def version(self):
        """Return RTP version"""
        return int(self.header[0] >> 6)
    
    def seqNum(self):
        """Return sequence number"""
        seqNum = self.header[2] << 8 | self.header[3]
        return int(seqNum)
    
    def timestamp(self):
        """Return timestamp"""
        timestamp = (self.header[4] << 24 | self.header[5] << 16 | 
                    self.header[6] << 8 | self.header[7])
        return int(timestamp)
    
    def payloadType(self):
        """Return payload type"""
        pt = self.header[1] & 0x7F
        return int(pt)
    
    def getPayload(self):
        """Return payload"""
        return self.payload
    
    def getPacket(self):
        """Return RTP packet (header + payload)"""
        return self.header + self.payload
