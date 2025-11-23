# 🎬 Video Streaming Server - RTSP & Web Interface

A comprehensive video streaming solution with both RTSP/RTP protocol support and a modern web-based interface. Built with Python, Flask, and HTML5.

![Video Streaming](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### Web Interface
- 🎨 **YouTube-style UI** - Modern, responsive dark theme
- 🎥 **Custom Video Player** - Built-in controls with keyboard shortcuts
- ⏩ **2-Second Seek Buttons** - Quick forward/backward navigation
- 🔊 **Smart Audio Handling** - Auto-unmute on interaction
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🌐 **Network Streaming** - Access from any device on your network

### RTSP/RTP Server
- 📡 **RTSP Protocol** - Industry-standard streaming protocol
- 🔄 **RTP Packets** - Real-time transport protocol
- 🖥️ **Tkinter Client** - Desktop GUI for video playback
- ⚡ **Frame-by-Frame Streaming** - Efficient video delivery

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/safiullah-foragy/Video_Streaming_RTSP.git
cd Video_Streaming_RTSP
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your videos:
```bash
# Place video files in assets/videos/ folder
# Supported formats: MP4, AVI, MOV, MKV, WebM, FLV, WMV, M4V
```

### Running the Server

#### Web Server (Recommended)
```bash
python web_server.py
```
Access at: `http://localhost:5000`

Or use the batch file:
```bash
start_web_server.bat
```

#### RTSP Server
```bash
# Start server
python Server.py

# In another terminal, start client
python Client.py
```

## 📖 Usage

### Web Interface

1. **Browse Videos**: Navigate to `http://localhost:5000` to see all available videos
2. **Watch Videos**: Click on any video thumbnail to start playing
3. **Controls**:
   - **Play/Pause**: Click video or press `Space`/`K`
   - **Seek ±2 sec**: Use arrow buttons or `←`/`→` keys
   - **Skip ±10 sec**: Press `Shift + ←/→` or `J`/`L`
   - **Volume**: Use slider or `↑`/`↓` keys
   - **Mute**: Press `M` or click volume button
   - **Fullscreen**: Press `F` or click fullscreen button

### Network Access
Share videos across your network:
```
http://YOUR_LOCAL_IP:5000
```
Example: `http://192.168.0.101:5000`

## 🌐 Live Deployment Options

### Option 1: PythonAnywhere (Free & Easy)
1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code
3. Set up a web app with Flask
4. Configure WSGI file
5. Your app will be live at `yourusername.pythonanywhere.com`

### Option 2: Heroku
1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn web_server:app
```
3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Option 3: Railway.app
1. Connect your GitHub repository
2. Railway auto-detects Flask
3. Deploy with one click

### Option 4: Render
1. Create account at [render.com](https://render.com)
2. Connect GitHub repository
3. Select "Web Service"
4. Deploy automatically

### Option 5: VPS (DigitalOcean, AWS, etc.)
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app
```

## 📁 Project Structure

```
Video_Streaming_RTSP/
├── web_server.py              # Flask web application
├── Server.py                  # RTSP server
├── Client.py                  # RTSP client with GUI
├── RtpPacket.py              # RTP packet handling
├── ServerWorker.py           # RTSP server worker
├── VideoStream.py            # Video streaming handler
├── assets/
│   └── videos/               # Video storage directory
├── static/
│   ├── css/
│   │   └── style.css        # Styling
│   └── js/
│       ├── main.js          # Video library
│       └── player.js        # Video player controls
├── templates/
│   ├── index.html           # Video library page
│   ├── player.html          # Video player page
│   └── 404.html             # Error page
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 3.1.2
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Video**: HTML5 Video API, OpenCV
- **Protocols**: RTSP, RTP, HTTP
- **Styling**: Custom CSS with dark theme

## 🎯 Key Features Explained

### Custom Video Controls
- Hover over video to show controls
- Visual notifications for seek and volume changes
- Progress bar with clickable seeking
- Time display (current/total)

### Smart Audio
- Starts muted (browser requirement)
- Auto-unmutes on first interaction
- Visual unmute notice
- Multiple unmute methods

### Network Streaming
- HTTP range requests for efficient seeking
- 1MB chunk streaming
- Support for large video files
- Cross-device compatibility

## 📝 Development

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Creating Sample Videos
```bash
python web_video_converter.py --sample
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in web_server.py
app.run(host='0.0.0.0', port=8080)
```

### Videos Not Playing
- Check video format (MP4 recommended)
- Ensure browser supports codec
- Try with different video file

### No Sound
- Click the unmute notice
- Check browser audio permissions
- Ensure video has audio track

## 📄 License

MIT License - feel free to use for personal or commercial projects.

## 👤 Author

**Safiullah Foragy**
- GitHub: [@safiullah-foragy](https://github.com/safiullah-foragy)

## 🙏 Acknowledgments

- HTML5 Video API
- Flask Framework
- Font Awesome Icons
- OpenCV Library

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

⭐ Star this repository if you find it helpful!
