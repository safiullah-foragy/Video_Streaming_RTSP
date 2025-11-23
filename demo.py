"""
Demo and Testing Script
Run various tests and demonstrations of the video streaming system
"""

import os
import sys
import time
import socket
import threading


class DemoHelper:
    """Helper class for demonstrations"""
    
    @staticmethod
    def print_header(title):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60 + "\n")
    
    @staticmethod
    def print_step(step_num, description):
        """Print formatted step"""
        print(f"\n[Step {step_num}] {description}")
        print("-" * 60)
    
    @staticmethod
    def check_file(filename):
        """Check if file exists"""
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✓ {filename} found ({size:,} bytes)")
            return True
        else:
            print(f"✗ {filename} not found")
            return False
    
    @staticmethod
    def check_port(host, port):
        """Check if port is available"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.bind((host, port))
            sock.close()
            print(f"✓ Port {port} is available")
            return True
        except:
            print(f"✗ Port {port} is already in use")
            return False
    
    @staticmethod
    def check_python_packages():
        """Check if required packages are installed"""
        packages = ['cv2', 'PIL', 'numpy']
        missing = []
        
        for package in packages:
            try:
                __import__(package)
                print(f"✓ {package} is installed")
            except ImportError:
                print(f"✗ {package} is NOT installed")
                missing.append(package)
        
        return len(missing) == 0


def system_check():
    """Perform system check"""
    DemoHelper.print_header("SYSTEM CHECK")
    
    print("Checking Python version...")
    print(f"✓ Python {sys.version.split()[0]}")
    
    print("\nChecking required packages...")
    packages_ok = DemoHelper.check_python_packages()
    
    if not packages_ok:
        print("\n⚠ Some packages are missing!")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\nChecking video file...")
    video_exists = DemoHelper.check_file('movie.Mjpeg')
    
    if not video_exists:
        print("\n⚠ Video file not found!")
        print("Run: python VideoConverter.py --test")
        return False
    
    print("\nChecking ports...")
    rtsp_ok = DemoHelper.check_port('127.0.0.1', 8554)
    rtp_ok = DemoHelper.check_port('127.0.0.1', 25000)
    
    if not rtsp_ok or not rtp_ok:
        print("\n⚠ Some ports are in use!")
        print("Close other instances or change ports in config.py")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All checks passed! System is ready.")
    print("=" * 60)
    return True


def show_project_structure():
    """Display project structure"""
    DemoHelper.print_header("PROJECT STRUCTURE")
    
    structure = """
    Video_Streaming_RTSP/
    │
    ├── 📄 Server.py              # RTSP server main entry
    ├── 📄 ServerWorker.py        # Client connection handler
    ├── 📄 Client.py              # RTSP client with GUI
    ├── 📄 RtpPacket.py          # RTP packet handler
    ├── 📄 VideoStream.py        # Video file operations
    ├── 📄 VideoConverter.py     # Video format converter
    ├── 📄 config.py             # Configuration settings
    │
    ├── 📄 requirements.txt      # Python dependencies
    ├── 📄 README.md            # Full documentation
    ├── 📄 QUICKSTART.md        # Quick start guide
    ├── 📄 TECHNICAL_DOC.md     # Technical details
    │
    ├── 🎬 movie.Mjpeg          # Video file (MJPEG format)
    │
    ├── 📜 start_server.bat     # Windows server launcher
    ├── 📜 start_client.bat     # Windows client launcher
    ├── 📜 start_server.sh      # Linux/Mac server launcher
    └── 📜 start_client.sh      # Linux/Mac client launcher
    """
    
    print(structure)


def show_protocol_flow():
    """Display protocol flow"""
    DemoHelper.print_header("RTSP/RTP PROTOCOL FLOW")
    
    flow = """
    CLIENT                          SERVER
      │                               │
      │─────── SETUP request ────────▶│
      │                          [Setup session]
      │◀──────── 200 OK ──────────────│
      │                               │
      │─────── PLAY request ─────────▶│
      │                    [Start streaming]
      │◀──────── 200 OK ──────────────│
      │                               │
      │◀═══ RTP Packet (Frame 1) ════│
      │◀═══ RTP Packet (Frame 2) ════│
      │◀═══ RTP Packet (Frame 3) ════│
      │             ...               │
      │                               │
      │─────── PAUSE request ────────▶│
      │                     [Stop streaming]
      │◀──────── 200 OK ──────────────│
      │                               │
      │─────── PLAY request ─────────▶│
      │                   [Resume streaming]
      │◀──────── 200 OK ──────────────│
      │                               │
      │─────── TEARDOWN request ─────▶│
      │                      [Cleanup]
      │◀──────── 200 OK ──────────────│
      │                               │
    
    Legend:
    ─────▶  RTSP control messages (TCP, port 8554)
    ═════▶  RTP video packets (UDP, port 25000)
    """
    
    print(flow)


def show_usage_guide():
    """Display usage guide"""
    DemoHelper.print_header("USAGE GUIDE")
    
    guide = """
    🚀 QUICK START:
    
    Step 1: Install Dependencies
    $ pip install -r requirements.txt
    
    Step 2: Create Test Video
    $ python VideoConverter.py --test
    
    Step 3: Start Server (Terminal 1)
    $ python Server.py
    
    Step 4: Start Client (Terminal 2)
    $ python Client.py
    
    
    🎮 CLIENT CONTROLS:
    
    ⚙ SETUP   - Connect to server and prepare streaming session
    ▶ PLAY    - Start video playback
    ⏸ PAUSE   - Pause video playback
    ⏹ STOP    - Stop and disconnect from server
    
    
    📊 STATISTICS DISPLAYED:
    
    • Status    - Current connection state
    • Frame     - Current frame number
    • Bitrate   - Data rate in kbps
    • FPS       - Actual frames per second
    
    
    🎥 USING YOUR OWN VIDEO:
    
    Convert any video file:
    $ python VideoConverter.py myvideo.mp4
    
    This creates movie.Mjpeg for streaming.
    
    
    🌐 NETWORK STREAMING:
    
    Server side (edit config.py):
    SERVER_HOST = '0.0.0.0'
    
    Client side:
    $ python Client.py <server_ip> 8554 25000 movie.Mjpeg
    """
    
    print(guide)


def show_menu():
    """Display main menu"""
    DemoHelper.print_header("VIDEO STREAMING RTSP/RTP - DEMO & TEST")
    
    print("""
    Please select an option:
    
    1. System Check (verify installation)
    2. Show Project Structure
    3. Show Protocol Flow
    4. Show Usage Guide
    5. Create Test Video
    6. Run All Checks
    
    0. Exit
    """)


def create_test_video():
    """Create test video"""
    DemoHelper.print_header("CREATE TEST VIDEO")
    
    print("Creating test video...")
    print("This may take a moment...\n")
    
    try:
        os.system('python VideoConverter.py --test')
        print("\n✓ Test video created successfully!")
        print("File: movie.Mjpeg")
    except Exception as e:
        print(f"\n✗ Error creating test video: {e}")


def run_all_checks():
    """Run all checks"""
    system_check()
    time.sleep(2)
    show_project_structure()
    time.sleep(2)
    show_protocol_flow()
    time.sleep(2)
    show_usage_guide()


def main():
    """Main demo loop"""
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == '0':
                print("\nGoodbye!")
                break
            elif choice == '1':
                system_check()
            elif choice == '2':
                show_project_structure()
            elif choice == '3':
                show_protocol_flow()
            elif choice == '4':
                show_usage_guide()
            elif choice == '5':
                create_test_video()
            elif choice == '6':
                run_all_checks()
            else:
                print("\n⚠ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            input("\nPress Enter to continue...")


if __name__ == '__main__':
    main()
