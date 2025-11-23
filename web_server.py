"""
Web-Based Video Streaming Server
Serves videos from assets/videos folder via HTTP with a YouTube-like web interface
"""

import os
import mimetypes
from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from pathlib import Path
import json

app = Flask(__name__)

# Configuration
VIDEOS_FOLDER = os.path.join(os.path.dirname(__file__), 'assets', 'videos')
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for streaming

# Ensure videos folder exists
os.makedirs(VIDEOS_FOLDER, exist_ok=True)

def get_video_files():
    """Get list of all video files in the assets/videos folder"""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v']
    videos = []
    
    if not os.path.exists(VIDEOS_FOLDER):
        return videos
    
    for filename in os.listdir(VIDEOS_FOLDER):
        file_path = os.path.join(VIDEOS_FOLDER, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            if ext in video_extensions:
                file_size = os.path.getsize(file_path)
                videos.append({
                    'filename': filename,
                    'name': os.path.splitext(filename)[0],
                    'size': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2),
                    'extension': ext[1:].upper()
                })
    
    return sorted(videos, key=lambda x: x['name'])


def get_video_stream(video_path, start=0, end=None):
    """Generate video stream with support for range requests"""
    file_size = os.path.getsize(video_path)
    
    if end is None:
        end = file_size - 1
    
    length = end - start + 1
    
    with open(video_path, 'rb') as video_file:
        video_file.seek(start)
        remaining = length
        
        while remaining > 0:
            chunk_size = min(CHUNK_SIZE, remaining)
            data = video_file.read(chunk_size)
            if not data:
                break
            remaining -= len(data)
            yield data


@app.route('/')
def index():
    """Main page - video browser"""
    return render_template('index.html')


@app.route('/api/videos')
def api_videos():
    """API endpoint to get list of available videos"""
    videos = get_video_files()
    return jsonify({
        'success': True,
        'count': len(videos),
        'videos': videos
    })


@app.route('/api/video/<path:filename>')
def stream_video(filename):
    """Stream video with support for range requests (seeking)"""
    video_path = os.path.join(VIDEOS_FOLDER, filename)
    
    if not os.path.exists(video_path):
        return jsonify({'success': False, 'error': 'Video not found'}), 404
    
    file_size = os.path.getsize(video_path)
    
    # Get range header if present
    range_header = request.headers.get('Range')
    
    if range_header:
        # Parse range header (e.g., "bytes=0-1023")
        byte_range = range_header.replace('bytes=', '').split('-')
        start = int(byte_range[0]) if byte_range[0] else 0
        end = int(byte_range[1]) if byte_range[1] else file_size - 1
        
        # Ensure end doesn't exceed file size
        end = min(end, file_size - 1)
        length = end - start + 1
        
        # Create response with partial content
        response = Response(
            get_video_stream(video_path, start, end),
            206,  # Partial Content
            mimetype=mimetypes.guess_type(filename)[0] or 'video/mp4',
            direct_passthrough=True
        )
        
        response.headers.add('Content-Range', f'bytes {start}-{end}/{file_size}')
        response.headers.add('Accept-Ranges', 'bytes')
        response.headers.add('Content-Length', str(length))
        
    else:
        # Full content
        response = Response(
            get_video_stream(video_path),
            200,
            mimetype=mimetypes.guess_type(filename)[0] or 'video/mp4',
            direct_passthrough=True
        )
        
        response.headers.add('Content-Length', str(file_size))
        response.headers.add('Accept-Ranges', 'bytes')
    
    # Add caching headers
    response.headers.add('Cache-Control', 'public, max-age=3600')
    
    return response


@app.route('/watch/<path:filename>')
def watch_video(filename):
    """Video player page"""
    video_path = os.path.join(VIDEOS_FOLDER, filename)
    
    if not os.path.exists(video_path):
        return "Video not found", 404
    
    video_info = {
        'filename': filename,
        'name': os.path.splitext(filename)[0],
        'size': os.path.getsize(video_path),
        'extension': os.path.splitext(filename)[1][1:].upper()
    }
    
    return render_template('player.html', video=video_info)


@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


def main():
    """Run the web server"""
    print("=" * 60)
    print("  🎬 Video Streaming Web Server")
    print("=" * 60)
    print()
    print(f"📁 Videos folder: {VIDEOS_FOLDER}")
    print(f"📹 Available videos: {len(get_video_files())}")
    print()
    print("🌐 Server starting on http://localhost:5000")
    print("   Open this URL in your web browser to access the video library")
    print()
    print("📝 To add videos: Place video files in assets/videos/ folder")
    print("   Supported formats: MP4, AVI, MOV, MKV, WebM, FLV, WMV, M4V")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Run Flask server
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)


if __name__ == '__main__':
    main()
