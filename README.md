# 🎬 Video Streaming Server

A comprehensive video streaming solution featuring **YouTube-style web interface** and RTSP/RTP protocol support. Stream videos across your network with custom controls, keyboard shortcuts, and beautiful dark theme UI.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)](https://github.com/safiullah-foragy/Video_Streaming_RTSP)

---

## 🌐 Live Demo

**🚀 Try it now:** [https://video-streaming-rtsp.onrender.com](https://video-streaming-rtsp.onrender.com)

> **Note**: Free tier may take 30-60 seconds to wake up after inactivity. Once loaded, streaming is instant!

---

## ✨ Features

### 🌐 Web Interface (Featured)
- **🎨 YouTube-Style UI** - Modern, responsive dark theme
- **🎥 Custom Video Player** - Professional controls with progress bar
- **⏩ 2-Second Seek Buttons** - Quick forward/backward navigation
- **🔊 Smart Audio Handling** - Auto-unmute on interaction
- **⌨️ Keyboard Shortcuts** - Full keyboard control
- **📱 Responsive Design** - Works on all devices
- **🌐 Network Streaming** - Access from anywhere on your network

### 📡 RTSP/RTP Protocol
- **🔴 RTSP Server** - Industry-standard protocol
- **📦 RTP Packets** - Real-time transport
- **🖥️ Desktop Client** - Tkinter GUI
- **⚡ Frame Streaming** - Efficient delivery

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/safiullah-foragy/Video_Streaming_RTSP.git
cd Video_Streaming_RTSP

# Install dependencies
pip install -r requirements.txt

# Add your videos to assets/videos/

# Run web server
python web_server.py
```

**Access at**: `http://localhost:5000`

---

## 🎮 Usage

### Web Interface Controls

| Action | Button | Keyboard |
|--------|--------|----------|
| Play/Pause | ▶️/⏸️ | `Space`, `K` |
| Seek ±2 sec | ⏪/⏩ | `←`/`→` |
| Skip ±10 sec | - | `Shift + ←/→`, `J`/`L` |
| Volume | 🔊 | `↑`/`↓` |
| Mute | 🔇 | `M` |
| Fullscreen | ⛶ | `F` |

---

## 🌐 Live Hosting

**Your code is ready to deploy!** Check [LIVE_HOSTING_GUIDE.md](LIVE_HOSTING_GUIDE.md) for detailed instructions.

### Recommended Platforms:
1. **PythonAnywhere** - Free, always-on, easiest setup
2. **Render.com** - Free tier with auto-deploy from GitHub
3. **Railway.app** - One-click deployment
4. **Heroku** - Classic platform ($5/month)

---

## 📁 Project Structure

```
Video_Streaming_RTSP/
├── web_server.py              # Flask web app ⭐
├── Server.py                  # RTSP server
├── Client.py                  # RTSP client GUI
├── assets/videos/             # Video storage 🎬
├── static/
│   ├── css/style.css         # YouTube-style theme
│   └── js/
│       ├── player.js         # Custom video player
│       └── main.js           # Video library
├── templates/
│   ├── index.html            # Video library page
│   └── player.html           # Video player page
└── requirements.txt           # Dependencies
```

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask 3.1.2
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Video**: HTML5 Video API, OpenCV
- **Protocols**: RTSP, RTP, HTTP
- **UI**: Custom dark theme, Font Awesome icons

---

## 📸 Screenshots

### Video Library
Beautiful grid layout with hover effects and video thumbnails.

### Video Player
Custom controls with 2-second seek buttons, progress bar, and volume control.

---

## 🎯 Key Features

### Custom Video Controls
- Hover to show controls
- Visual seek notifications (+2s, -2s)
- Clickable progress bar
- Real-time display

### Smart Audio
- Starts muted (browser requirement)
- Auto-unmutes on interaction
- Visual unmute notice
- Multiple unmute methods

### Network Streaming
- HTTP range requests
- 1MB chunk streaming
- Large file support
- Cross-device compatible

---

## 📖 Documentation

- **[LIVE_HOSTING_GUIDE.md](LIVE_HOSTING_GUIDE.md)** - Deploy to production
- **[WEB_QUICKSTART.md](WEB_QUICKSTART.md)** - Web interface guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Detailed deployment

---

## 🐛 Troubleshooting

### Port Already in Use
```python
# Change port in web_server.py
app.run(host='0.0.0.0', port=8080)
```

### Videos Not Playing
- Use MP4 format (H.264 codec)
- Check browser compatibility
- Ensure video has valid codec

### No Sound
- Click unmute notice
- Check browser permissions
- Verify audio track exists

---

## 🚀 Deployment

Your Flask app can be deployed to:

```bash
# PythonAnywhere (Recommended)
# 1. Upload code
# 2. Set up Flask web app
# 3. Configure WSGI
# Live at: yourusername.pythonanywhere.com

# Render.com
# 1. Connect GitHub
# 2. Auto-deploy
# Live at: your-app.onrender.com

# Railway.app
# 1. Import repo
# 2. One-click deploy
# Live at: your-app.up.railway.app
```

See **[LIVE_HOSTING_GUIDE.md](LIVE_HOSTING_GUIDE.md)** for step-by-step instructions!

---

## 🤝 Contributing

Contributions welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📄 License

MIT License - Use freely for personal or commercial projects.

---

## 👤 Author

**Safiullah Foragy**
- GitHub: [@safiullah-foragy](https://github.com/safiullah-foragy)
- Repository: [Video_Streaming_RTSP](https://github.com/safiullah-foragy/Video_Streaming_RTSP)

---

## 🙏 Acknowledgments

- HTML5 Video API
- Flask Framework
- Font Awesome Icons
- OpenCV Library

---

## ⭐ Support

If you find this project helpful, please give it a star on GitHub!

**Questions?** Open an issue or check the documentation files.

---

**Ready to stream? 🎬 Start the server and enjoy!**
