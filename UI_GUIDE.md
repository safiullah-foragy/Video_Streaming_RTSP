# Visual UI Guide - Video Streaming Client

## 🎨 YouTube-Style Interface

### Full Window Layout

```
┌────────────────────────────────────────────────────────────────┐
│  🎬 Video Streaming Player                                      │  ← Title Bar
│                                                                 │    (Dark theme)
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│                                                                 │
│                                                                 │
│                    [Video Display Area]                         │  ← Video Display
│                                                                 │    (640 x 480)
│                         640 x 480                               │    Black background
│                                                                 │
│                                                                 │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│  ══════════════════════════════════════════════════════════    │  ← Progress Bar
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│      ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │  ← Control Buttons
│      │⚙ SETUP │  │ ▶ PLAY  │  │ ⏸ PAUSE │  │ ⏹ STOP  │      │    (Clickable)
│      └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│  Status: Playing  |  Frame: 245  |  Bitrate: 1250 kbps  |     │  ← Status Bar
│  FPS: 24.0                                                      │    (Real-time info)
└────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Color Scheme

### Background Colors
```
Main Background:     #181818  (Very Dark Gray)
Panel Background:    #212121  (Dark Gray)
Control Panel:       #282828  (Medium Dark Gray)
Video Area:          #000000  (Pure Black)
```

### Button Colors
```
⚙ SETUP Button:      #3EA6FF  (Blue)
▶ PLAY Button:       #FF0000  (YouTube Red)
⏸ PAUSE Button:      #909090  (Gray)
⏹ STOP Button:       #606060  (Dark Gray)
```

### Text Colors
```
Primary Text:        #FFFFFF  (White)
Secondary Text:      #AAAAAA  (Light Gray)
```

---

## 📐 Dimensions

### Window
- **Default Size**: 900 x 700 pixels
- **Resizable**: Yes
- **Minimum Size**: 800 x 600 pixels

### Components
- **Title Bar**: Full width, 60px height
- **Video Display**: 640 x 480 pixels (centered)
- **Progress Bar**: Full width, 30px height
- **Control Panel**: Full width, 120px height
- **Status Bar**: Full width, 50px height

### Buttons
- **Width**: 12 characters
- **Height**: 2 lines
- **Spacing**: 5px between buttons
- **Font**: Helvetica 11pt Bold

---

## 🎮 Button States

### ⚙ SETUP Button

**Initial State:**
```
┌─────────────┐
│  ⚙ SETUP   │  ← Blue (#3EA6FF)
└─────────────┘    Enabled
```

**After Setup:**
```
┌─────────────┐
│  ⚙ SETUP   │  ← Grayed out
└─────────────┘    Disabled
```

### ▶ PLAY Button

**Initial State:**
```
┌─────────────┐
│  ▶ PLAY    │  ← Grayed out
└─────────────┘    Disabled
```

**After Setup:**
```
┌─────────────┐
│  ▶ PLAY    │  ← Red (#FF0000)
└─────────────┘    Enabled, Ready to click
```

**While Playing:**
```
┌─────────────┐
│  ▶ PLAY    │  ← Grayed out
└─────────────┘    Disabled
```

### ⏸ PAUSE Button

**Before Playing:**
```
┌─────────────┐
│  ⏸ PAUSE   │  ← Grayed out
└─────────────┘    Disabled
```

**While Playing:**
```
┌─────────────┐
│  ⏸ PAUSE   │  ← Active (#909090)
└─────────────┘    Enabled, clickable
```

### ⏹ STOP Button

**Before Setup:**
```
┌─────────────┐
│  ⏹ STOP    │  ← Grayed out
└─────────────┘    Disabled
```

**After Setup:**
```
┌─────────────┐
│  ⏹ STOP    │  ← Active (#606060)
└─────────────┘    Enabled, clickable
```

---

## 📊 Status Bar Display

### Connection States

**Not Connected:**
```
Status: Not Connected  |  Frame: 0  |  Bitrate: 0 kbps  |  FPS: 0
```

**Connecting:**
```
Status: Connecting to server...  |  Frame: 0  |  Bitrate: 0 kbps  |  FPS: 0
```

**Ready:**
```
Status: Ready  |  Frame: 0  |  Bitrate: 0 kbps  |  FPS: 0
```

**Playing:**
```
Status: Playing...  |  Frame: 245  |  Bitrate: 1250 kbps  |  FPS: 24.0
```

**Paused:**
```
Status: Paused  |  Frame: 245  |  Bitrate: 1250 kbps  |  FPS: 24.0
```

**Disconnecting:**
```
Status: Disconnecting...  |  Frame: 245  |  Bitrate: 1250 kbps  |  FPS: 24.0
```

---

## 🎬 Video Display States

### No Connection (Initial)
```
┌────────────────────────────────────┐
│                                    │
│                                    │
│          [Empty Black Screen]      │
│                                    │
│                                    │
└────────────────────────────────────┘
```

### After Setup (Ready)
```
┌────────────────────────────────────┐
│                                    │
│                                    │
│          [Still Black Screen]      │
│          Waiting for PLAY...       │
│                                    │
└────────────────────────────────────┘
```

### Playing (Active Streaming)
```
┌────────────────────────────────────┐
│     ╔════════════════════╗        │
│     ║                    ║        │
│     ║   [Video Frame]    ║        │
│     ║    Streaming...    ║        │
│     ║                    ║        │
│     ╚════════════════════╝        │
└────────────────────────────────────┘
```

---

## 🖱️ User Interaction Flow

### Typical Usage Sequence

```
1. Application Starts
   │
   ↓
2. User clicks "⚙ SETUP"
   │
   ├─→ Connects to server
   ├─→ Establishes session
   └─→ Status: "Ready"
   │
   ↓
3. User clicks "▶ PLAY"
   │
   ├─→ Starts RTP reception
   ├─→ Displays video frames
   └─→ Status: "Playing..."
   │
   ↓
4. User watches video
   │
   ├─→ Real-time stats update
   ├─→ Frames displayed continuously
   └─→ Progress bar moves
   │
   ↓
5. User clicks "⏸ PAUSE"
   │
   ├─→ Stops RTP reception
   ├─→ Freezes current frame
   └─→ Status: "Paused"
   │
   ↓
6. User clicks "▶ PLAY" again
   │
   ├─→ Resumes streaming
   └─→ Status: "Playing..."
   │
   ↓
7. User clicks "⏹ STOP"
   │
   ├─→ Stops streaming
   ├─→ Disconnects from server
   ├─→ Clears video display
   └─→ Application closes
```

---

## 🎯 Interactive Elements

### Clickable Buttons

All buttons change appearance on hover and click:

**Normal State:**
```
┌─────────────┐
│  ▶ PLAY    │
└─────────────┘
```

**Hover State:**
```
┌─────────────┐
│  ▶ PLAY    │  ← Slightly brighter
└─────────────┘    Cursor: hand pointer
```

**Clicked State:**
```
┌─────────────┐
│  ▶ PLAY    │  ← Pressed appearance
└─────────────┘    (relief changes)
```

**Disabled State:**
```
┌─────────────┐
│  ▶ PLAY    │  ← Grayed out
└─────────────┘    No interaction
```

---

## 📱 Responsive Design

### Window Resizing

The interface adapts when window is resized:

**Minimum Size (800x600):**
```
┌──────────────────────────────┐
│  🎬 Video Streaming Player   │
├──────────────────────────────┤
│   [Video: 640x480]          │
├──────────────────────────────┤
│  ════════════════            │
├──────────────────────────────┤
│  [SETUP][PLAY][PAUSE][STOP]  │
├──────────────────────────────┤
│  Status | Frame | Bitrate    │
└──────────────────────────────┘
```

**Larger Window (1200x800):**
```
┌──────────────────────────────────────────┐
│     🎬 Video Streaming Player            │
├──────────────────────────────────────────┤
│                                          │
│        [Video: 640x480 - Centered]       │
│                                          │
├──────────────────────────────────────────┤
│  ══════════════════════════════════════  │
├──────────────────────────────────────────┤
│   [SETUP]  [PLAY]  [PAUSE]  [STOP]       │
├──────────────────────────────────────────┤
│  Status | Frame | Bitrate | FPS          │
└──────────────────────────────────────────┘
```

---

## 🌈 Visual Feedback

### Connection Progress

When connecting, visual feedback is provided:

1. **Button Press**: Button appears pressed
2. **Status Update**: "Connecting to server..."
3. **Success**: Status changes to "Ready"
4. **Button States**: PLAY and STOP buttons activate

### Streaming Feedback

When streaming:

1. **Video Updates**: 24 frames per second
2. **Frame Counter**: Increments continuously
3. **Bitrate Display**: Updates every second
4. **FPS Display**: Real-time calculation

### Error Feedback

If errors occur:

1. **Error Dialog**: Pop-up message box
2. **Status Update**: Shows error message
3. **Button Reset**: Returns to initial state

---

## 💡 Tips for Best Experience

### Display
- Video is best viewed at default size (640x480)
- Dark theme reduces eye strain
- Status bar provides useful debugging info

### Performance
- Local network: Smooth playback at 24 FPS
- Over internet: May vary based on bandwidth
- Statistics help diagnose issues

### Navigation
- Use SETUP only once per session
- PLAY/PAUSE can be toggled freely
- STOP closes the connection completely

---

## 🎓 GUI Design Principles Used

### 1. **Consistency**
- YouTube-inspired familiar layout
- Consistent button styling
- Predictable behavior

### 2. **Feedback**
- Visual button states
- Status bar updates
- Real-time statistics

### 3. **Simplicity**
- Clear, labeled buttons
- Intuitive workflow
- Minimal clutter

### 4. **Aesthetics**
- Modern dark theme
- Professional appearance
- Color-coded buttons

---

*This guide helps you understand the visual design and user interaction of the video streaming client.*
