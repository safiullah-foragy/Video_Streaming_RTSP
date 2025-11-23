"""
Video Converter Utility
Converts standard video files to MJPEG format for streaming
"""

import cv2
import sys


def convert_video_to_mjpeg(input_file, output_file='movie.Mjpeg'):
    """
    Convert a video file to MJPEG format suitable for streaming
    
    Args:
        input_file: Path to input video file (mp4, avi, etc.)
        output_file: Path to output MJPEG file
    """
    print(f"Converting {input_file} to MJPEG format...")
    
    # Open the video file
    cap = cv2.VideoCapture(input_file)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_file}")
        return False
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Video properties: {frame_count} frames at {fps} FPS")
    
    # Open output file
    with open(output_file, 'wb') as f:
        frame_num = 0
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Encode frame as JPEG
            ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            
            if ret:
                # Get frame data
                frame_data = jpeg.tobytes()
                frame_length = len(frame_data)
                
                # Write frame length (5 bytes) followed by frame data
                f.write(str(frame_length).zfill(5).encode())
                f.write(frame_data)
                
                frame_num += 1
                if frame_num % 10 == 0:
                    print(f"Processed {frame_num}/{frame_count} frames", end='\r')
            else:
                print(f"\nWarning: Failed to encode frame {frame_num}")
        
        print(f"\nConversion complete! Created {output_file} with {frame_num} frames")
    
    cap.release()
    return True


def create_test_video(output_file='movie.Mjpeg', duration=10, fps=24):
    """
    Create a simple test video with animated content
    
    Args:
        output_file: Path to output MJPEG file
        duration: Duration in seconds
        fps: Frames per second
    """
    import numpy as np
    
    print(f"Creating test video: {duration}s at {fps} FPS")
    
    width, height = 640, 480
    total_frames = duration * fps
    
    with open(output_file, 'wb') as f:
        for frame_num in range(total_frames):
            # Create frame with changing colors and text
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Animated background color
            color_val = int((frame_num / total_frames) * 255)
            frame[:, :] = (color_val, 100, 255 - color_val)
            
            # Add frame number text
            cv2.putText(frame, f'Frame {frame_num + 1}/{total_frames}', 
                       (50, height // 2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       1.5, (255, 255, 255), 3)
            
            # Add progress bar
            bar_width = int((frame_num / total_frames) * (width - 100))
            cv2.rectangle(frame, (50, height - 100), 
                         (50 + bar_width, height - 80), 
                         (0, 255, 0), -1)
            
            # Encode as JPEG
            ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            
            if ret:
                frame_data = jpeg.tobytes()
                frame_length = len(frame_data)
                
                # Write frame
                f.write(str(frame_length).zfill(5).encode())
                f.write(frame_data)
                
                if (frame_num + 1) % 10 == 0:
                    print(f"Created {frame_num + 1}/{total_frames} frames", end='\r')
        
        print(f"\nTest video created: {output_file}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Video Converter Utility")
        print("\nUsage:")
        print("  python VideoConverter.py <input_video>           - Convert existing video")
        print("  python VideoConverter.py --test                  - Create test video")
        print("\nExamples:")
        print("  python VideoConverter.py myvideo.mp4")
        print("  python VideoConverter.py --test")
        return
    
    if sys.argv[1] == '--test':
        # Create test video
        create_test_video('movie.Mjpeg', duration=10, fps=24)
    else:
        # Convert existing video
        input_file = sys.argv[1]
        output_file = 'movie.Mjpeg'
        
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        
        convert_video_to_mjpeg(input_file, output_file)


if __name__ == '__main__':
    main()
