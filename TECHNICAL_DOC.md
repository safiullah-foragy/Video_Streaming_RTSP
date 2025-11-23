# Video Streaming System - Technical Documentation

## 🏗️ System Architecture

### Overview
This system implements a client-server video streaming application using:
- **RTSP (RFC 2326)** for session control over TCP
- **RTP (RFC 3550)** for real-time video data over UDP
- **MJPEG** format for video encoding

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌────────────────────────┐        │
│  │  GUI Layer   │────────▶│  Client.py             │        │
│  │  (Tkinter)   │         │  - RTSP Client         │        │
│  └──────────────┘         │  - RTP Receiver        │        │
│                           │  - Frame Display       │        │
│                           └────────┬───────────────┘        │
│                                    │                         │
│                                    │ RTSP (TCP)              │
│                                    │ RTP (UDP)               │
└────────────────────────────────────┼─────────────────────────┘
                                     │
                                     │ Port 8554 (RTSP)
                                     │ Port 25000 (RTP)
                                     │
┌────────────────────────────────────┼─────────────────────────┐
│                         SERVER SIDE │                         │
├────────────────────────────────────┴─────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌────────────────────────┐        │
│  │  Server.py   │────────▶│  ServerWorker.py       │        │
│  │  Main Loop   │         │  - RTSP Handler        │        │
│  └──────────────┘         │  - Session Manager     │        │
│                           │  - RTP Sender          │        │
│                           └────────┬───────────────┘        │
│                                    │                         │
│                           ┌────────▼───────────────┐        │
│                           │  VideoStream.py        │        │
│                           │  - Frame Reader        │        │
│                           │  - File Handler        │        │
│                           └────────┬───────────────┘        │
│                                    │                         │
│                           ┌────────▼───────────────┐        │
│                           │  RtpPacket.py          │        │
│                           │  - Packet Encoding     │        │
│                           │  - Header Creation     │        │
│                           └────────────────────────┘        │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## 🔄 Protocol Flow

### Session Establishment (SETUP)

```
Client                                    Server
  │                                         │
  │─────── TCP Connection ─────────────────▶│
  │                                         │
  │  SETUP movie.Mjpeg RTSP/1.0            │
  │  CSeq: 1                               │
  │  Transport: RTP/UDP; client_port=25000 │
  │────────────────────────────────────────▶│
  │                                         │
  │                                   [Allocate Resources]
  │                                   [Create VideoStream]
  │                                   [Generate Session ID]
  │                                         │
  │  RTSP/1.0 200 OK                       │
  │  CSeq: 1                               │
  │  Session: 123456                       │
  │◀────────────────────────────────────────│
  │                                         │
```

### Playing Video (PLAY)

```
Client                                    Server
  │                                         │
  │  PLAY movie.Mjpeg RTSP/1.0             │
  │  CSeq: 2                               │
  │  Session: 123456                       │
  │────────────────────────────────────────▶│
  │                                         │
  │                                   [Start RTP Thread]
  │                                   [Send Frames]
  │                                         │
  │  RTSP/1.0 200 OK                       │
  │  CSeq: 2                               │
  │◀────────────────────────────────────────│
  │                                         │
  │◀═══════ RTP Packet (Frame 1) ══════════│
  │◀═══════ RTP Packet (Frame 2) ══════════│
  │◀═══════ RTP Packet (Frame 3) ══════════│
  │                ...                      │
```

### Pausing Stream (PAUSE)

```
Client                                    Server
  │                                         │
  │  PAUSE movie.Mjpeg RTSP/1.0            │
  │  CSeq: 3                               │
  │  Session: 123456                       │
  │────────────────────────────────────────▶│
  │                                         │
  │                                   [Stop RTP Thread]
  │                                         │
  │  RTSP/1.0 200 OK                       │
  │  CSeq: 3                               │
  │◀────────────────────────────────────────│
  │                                         │
  [No more RTP packets]                     │
```

### Terminating Session (TEARDOWN)

```
Client                                    Server
  │                                         │
  │  TEARDOWN movie.Mjpeg RTSP/1.0         │
  │  CSeq: 4                               │
  │  Session: 123456                       │
  │────────────────────────────────────────▶│
  │                                         │
  │                                   [Stop RTP Thread]
  │                                   [Close VideoStream]
  │                                   [Free Resources]
  │                                         │
  │  RTSP/1.0 200 OK                       │
  │  CSeq: 4                               │
  │◀────────────────────────────────────────│
  │                                         │
  │─────── Close Connection ───────────────▶│
```

## 📦 Component Details

### 1. RtpPacket.py

**Purpose:** Handles RTP packet creation and parsing

**Key Methods:**
- `encode()` - Creates RTP packet with header and payload
- `decode()` - Parses received RTP packet
- `getPayload()` - Extracts video frame data
- `seqNum()` - Returns packet sequence number

**RTP Header Format (12 bytes):**
```
Byte 0:    V(2) P(1) X(1) CC(4)
Byte 1:    M(1) PT(7)
Bytes 2-3: Sequence Number
Bytes 4-7: Timestamp
Bytes 8-11: SSRC
```

### 2. VideoStream.py

**Purpose:** Manages video file reading and frame extraction

**Key Methods:**
- `nextFrame()` - Reads next frame from file
- `frameNbr()` - Returns current frame number
- `reset()` - Resets to beginning of file

**MJPEG File Format:**
```
[5 bytes: frame length][frame data][5 bytes: frame length][frame data]...
```

### 3. ServerWorker.py

**Purpose:** Handles individual client connections

**State Machine:**
```
INIT ──SETUP──▶ READY ──PLAY──▶ PLAYING
                  ▲        │         │
                  │        │         │
                  └────────┴─PAUSE───┘
```

**Key Methods:**
- `processRtspRequest()` - Parses and handles RTSP commands
- `sendRtp()` - Continuously sends video frames via RTP
- `replyRtsp()` - Sends RTSP responses to client

### 4. Server.py

**Purpose:** Main server accepting client connections

**Workflow:**
1. Create TCP socket on port 8554
2. Listen for incoming connections
3. For each client, spawn ServerWorker thread
4. Handle multiple clients concurrently

### 5. Client.py

**Purpose:** RTSP client with GUI

**Components:**
- **GUI Layer:** Tkinter-based YouTube-style interface
- **RTSP Handler:** Sends control commands via TCP
- **RTP Receiver:** Receives video frames via UDP
- **Display Engine:** Renders frames using PIL/ImageTk

**Threading:**
- Main thread: GUI and RTSP communication
- RTP thread: Receives and displays video frames

## 🎨 GUI Design

### Layout Structure

```
┌─────────────────────────────────────────────────────┐
│                   Title Bar                         │
│            🎬 Video Streaming Player                │
├─────────────────────────────────────────────────────┤
│                                                     │
│                                                     │
│              Video Display Area                     │
│                  (640 x 480)                        │
│                                                     │
│                                                     │
├─────────────────────────────────────────────────────┤
│  ═══════════════════════════════════════════════   │  Progress Bar
├─────────────────────────────────────────────────────┤
│                                                     │
│    [SETUP]  [PLAY]  [PAUSE]  [STOP]               │  Control Buttons
│                                                     │
├─────────────────────────────────────────────────────┤
│  Status: Playing | Frame: 245 | Bitrate: 1250 kbps │  Status Bar
│  FPS: 24                                           │
└─────────────────────────────────────────────────────┘
```

### Color Scheme (Dark Theme)

- **Background:** #181818 (Dark Gray)
- **Panel Background:** #212121 (Lighter Gray)
- **Control Panel:** #282828 (Medium Gray)
- **Play Button:** #FF0000 (YouTube Red)
- **Setup Button:** #3EA6FF (Blue)
- **Text:** #FFFFFF (White)
- **Secondary Text:** #AAAAAA (Light Gray)

## 📊 Data Flow

### Video Frame Pipeline

```
1. VIDEO FILE (movie.Mjpeg)
         ↓
2. VideoStream.nextFrame()
   - Read 5 bytes (frame length)
   - Read frame data (JPEG)
         ↓
3. RtpPacket.encode()
   - Create RTP header
   - Attach JPEG payload
         ↓
4. UDP Socket.sendto()
   - Send packet to client
         ↓
5. Client UDP Socket.recv()
   - Receive RTP packet
         ↓
6. RtpPacket.decode()
   - Parse RTP header
   - Extract JPEG payload
         ↓
7. PIL Image.open()
   - Decode JPEG
   - Resize if needed
         ↓
8. ImageTk.PhotoImage()
   - Convert to Tkinter format
         ↓
9. Label.configure()
   - Display on screen
```

## 🔧 Configuration Parameters

### Network Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| SERVER_HOST | 127.0.0.1 | Server IP address |
| RTSP_PORT | 8554 | RTSP control port (TCP) |
| RTP_PORT | 25000 | RTP data port (UDP) |

### Video Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| VIDEO_FILE | movie.Mjpeg | Video filename |
| FRAME_RATE | 24 | Frames per second |
| MAX_PACKET_SIZE | 20480 | Maximum RTP packet size (bytes) |

### RTSP Configuration

| Parameter | Values | Description |
|-----------|--------|-------------|
| RTSP_VER | RTSP/1.0 | RTSP protocol version |
| Response Codes | 200, 404, 500 | HTTP-style status codes |

## 🧪 Testing Scenarios

### 1. Basic Functionality Test
- Start server
- Start client
- SETUP → PLAY → PAUSE → PLAY → TEARDOWN
- Verify smooth video playback

### 2. Multiple Client Test
- Start server
- Start 3 clients simultaneously
- All clients should play independently

### 3. Network Interruption Test
- Start streaming
- Disconnect network briefly
- Reconnect
- Verify error handling

### 4. Long Duration Test
- Stream video for 30+ minutes
- Monitor memory usage
- Check for memory leaks

### 5. Video Format Test
- Test with different video resolutions
- Test with various JPEG quality levels
- Verify performance differences

## 📈 Performance Metrics

### Typical Performance

- **Bitrate:** 800-1500 kbps (depends on video content)
- **Frame Rate:** 24 FPS (configurable)
- **Latency:** < 100ms on local network
- **CPU Usage:** 5-15% (client), 10-20% (server)
- **Memory:** ~50MB (client), ~30MB (server)

### Optimization Tips

1. **Reduce JPEG Quality:** Lower quality = smaller packets
2. **Adjust Frame Rate:** 15-20 FPS may be sufficient
3. **Use Efficient Video Resolution:** 640x480 or 480x360
4. **Network Tuning:** Increase UDP buffer size for high-bandwidth

## 🐛 Common Issues and Solutions

### Issue: Choppy Video

**Causes:**
- Network congestion
- CPU overload
- Frame rate mismatch

**Solutions:**
- Reduce frame rate in `config.py`
- Lower video resolution
- Check network bandwidth

### Issue: High Latency

**Causes:**
- Large packet sizes
- Network routing

**Solutions:**
- Decrease MAX_PACKET_SIZE
- Use wired connection instead of WiFi
- Run on local network

### Issue: Packets Out of Order

**Note:** Current implementation doesn't handle reordering

**Solutions:**
- Implement packet reordering buffer
- Use TCP instead of UDP (sacrifices real-time)
- Accept occasional artifacts

## 🔐 Security Considerations

### Current Limitations

⚠️ **This is an educational implementation with NO security features:**

- No authentication
- No encryption
- No access control
- Plain-text protocol

### Production Recommendations

For a production system, implement:

1. **Authentication:** RTSP Digest Authentication
2. **Encryption:** SRTP (Secure RTP)
3. **Access Control:** Session tokens, user permissions
4. **TLS/SSL:** Encrypt RTSP signaling
5. **Firewall Rules:** Restrict ports and IPs

## 📚 References

### RFCs and Standards

- **RFC 2326:** Real Time Streaming Protocol (RTSP)
- **RFC 3550:** RTP: A Transport Protocol for Real-Time Applications
- **RFC 2435:** RTP Payload Format for JPEG-compressed Video

### Resources

- RTSP Specification: https://tools.ietf.org/html/rfc2326
- RTP Specification: https://tools.ietf.org/html/rfc3550
- Python Socket Programming: https://docs.python.org/3/library/socket.html
- Tkinter Documentation: https://docs.python.org/3/library/tkinter.html

## 🎓 Educational Value

### Learning Outcomes

Students completing this project will understand:

1. **Network Programming:**
   - TCP vs UDP protocols
   - Client-server architecture
   - Socket programming in Python

2. **Multimedia Streaming:**
   - Real-time data transmission
   - Frame-based video encoding
   - Packet loss handling

3. **Protocol Implementation:**
   - Protocol state machines
   - Request-response patterns
   - Session management

4. **GUI Development:**
   - Event-driven programming
   - Multi-threaded applications
   - User interface design

5. **System Design:**
   - Component separation
   - Threading and concurrency
   - Error handling

---

**Last Updated:** November 2025
**Version:** 1.0
