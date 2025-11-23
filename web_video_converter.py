"""
Video Format Converter for Web Streaming
Converts videos to web-compatible MP4 format
"""

import cv2
import sys
import os
from pathlib import Path


def convert_to_web_format(input_file, output_file=None):
    """
    Convert video to web-compatible MP4 format
    
    Args:
        input_file: Path to input video file
        output_file: Path to output video file (optional)
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return False
    
    # Generate output filename if not provided
    if output_file is None:
        input_name = Path(input_file).stem
        output_file = os.path.join('assets', 'videos', f'{input_name}_web.mp4')
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"Converting: {input_file}")
    print(f"Output: {output_file}")
    print()
    
    # Open input video
    cap = cv2.VideoCapture(input_file)
    
    if not cap.isOpened():
        print(f"Error: Cannot open video file '{input_file}'")
        return False
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Input video: {width}x{height} @ {fps} FPS, {frame_count} frames")
    
    # Use MP4V codec (widely supported)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("Error: Cannot create output video file")
        cap.release()
        return False
    
    # Convert frame by frame
    frame_num = 0
    print()
    print("Converting... (this may take a while)")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        out.write(frame)
        frame_num += 1
        
        # Progress indicator
        if frame_num % 30 == 0:
            progress = (frame_num / frame_count) * 100
            print(f"Progress: {frame_num}/{frame_count} frames ({progress:.1f}%)", end='\r')
    
    print(f"\nConversion complete! Created: {output_file}")
    print(f"Processed {frame_num} frames")
    
    # Clean up
    cap.release()
    out.release()
    
    return True


def create_sample_video(output_file='assets/videos/sample_video.mp4', duration=10, fps=24):
    """
    Create a sample test video
    
    Args:
        output_file: Path to output video
        duration: Duration in seconds
        fps: Frames per second
    """
    import numpy as np
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"Creating sample video: {duration}s at {fps} FPS")
    print(f"Output: {output_file}")
    print()
    
    width, height = 1280, 720
    total_frames = duration * fps
    
    # Use MP4V codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("Error: Cannot create output video file")
        return False
    
    for frame_num in range(total_frames):
        # Create animated frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Animated background
        progress = frame_num / total_frames
        
        # Color gradient based on progress
        r = int(progress * 255)
        g = int((1 - progress) * 255)
        b = 150
        
        frame[:, :] = (b, g, r)
        
        # Add text
        time_sec = frame_num / fps
        text = f'Sample Video - {time_sec:.1f}s'
        cv2.putText(frame, text, (width//2 - 200, height//2 - 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        
        # Frame number
        frame_text = f'Frame {frame_num + 1} / {total_frames}'
        cv2.putText(frame, frame_text, (width//2 - 150, height//2 + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Progress bar
        bar_width = int((progress * (width - 200)))
        cv2.rectangle(frame, (100, height - 150), 
                     (100 + bar_width, height - 120), 
                     (0, 255, 0), -1)
        cv2.rectangle(frame, (100, height - 150), 
                     (width - 100, height - 120), 
                     (255, 255, 255), 2)
        
        # Write frame
        out.write(frame)
        
        if (frame_num + 1) % 30 == 0:
            print(f"Created {frame_num + 1}/{total_frames} frames", end='\r')
    
    print(f"\nSample video created: {output_file}")
    out.release()
    
    return True


def main():
    """Main entry point"""
    print("=" * 60)
    print("  Video Format Converter for Web Streaming")
    print("=" * 60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python web_video_converter.py <input_video>")
        print("  python web_video_converter.py --sample")
        print()
        print("Examples:")
        print("  python web_video_converter.py myvideo.avi")
        print("  python web_video_converter.py --sample")
        print()
        return
    
    if sys.argv[1] == '--sample':
        # Create sample video
        duration = 15
        if len(sys.argv) > 2:
            try:
                duration = int(sys.argv[2])
            except:
                pass
        
        create_sample_video(duration=duration)
    else:
        # Convert existing video
        input_file = sys.argv[1]
        output_file = None
        
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        
        convert_to_web_format(input_file, output_file)
    
    print()
    print("=" * 60)
    print("Done! Video is ready for web streaming.")
    print("Start the server with: python web_server.py")
    print("=" * 60)


if __name__ == '__main__':
    main()
