# 🏗️ AutoReelBot Architecture Guide

## Table of Contents

- [System Overview](#system-overview)
- [Core Modules](#core-modules)
- [Data Flow](#data-flow)
- [Technical Stack](#technical-stack)
- [Design Decisions](#design-decisions)
- [Scalability Considerations](#scalability-considerations)

---

## System Overview

AutoReelBot is designed as a **modular, pipeline-based automation system** that transforms text prompts into polished Instagram Reels through a series of discrete processing stages.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                          (main.py)                              │
│                                                                 │
│  Entry Point → Orchestrates all modules → Handles errors       │
└────────────┬────────────────────────────────────┬───────────────┘
             │                                    │
             │                                    │
    ┌────────▼─────────┐                 ┌────────▼──────────┐
    │  CONTENT ENGINE  │                 │  INSTAGRAM MODULE │
    │   (Gemini AI)    │                 │    (login.py)     │
    │                  │                 │                   │
    │  • Theme select  │                 │  • Authentication │
    │  • Script gen    │                 │  • Upload         │
    │  • Caption gen   │                 │  • Session mgmt   │
    │  • Hashtag gen   │                 │  • Error handling │
    └────────┬─────────┘                 └───────────────────┘
             │
             │
    ┌────────▼──────────────────────────────────────────────┐
    │           VIDEO PRODUCTION MODULE                     │
    │              (video_editor.py)                        │
    │                                                       │
    │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
    │  │ Voice Engine │  │ Image Engine │  │ Audio Mix  │ │
    │  │  (EdgeTTS)   │  │  (Filters +  │  │  (Voice +  │ │
    │  │              │  │   Ken Burns) │  │   Music)   │ │
    │  └──────────────┘  └──────────────┘  └────────────┘ │
    │                                                       │
    │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
    │  │  Transition  │  │   Compositor │  │  Renderer  │ │
    │  │   Manager    │  │  (Clip Merge)│  │  (Export)  │ │
    │  └──────────────┘  └──────────────┘  └────────────┘ │
    └───────────────────────────────────────────────────────┘
```

### Key Principles

1. **Separation of Concerns**: Each module handles a specific domain (content, video, upload)
2. **Fail-Fast**: Errors are caught early and reported clearly
3. **Resource Efficiency**: Temporary files are cleaned up automatically
4. **Modularity**: Components can be used independently or combined
5. **Extensibility**: Easy to add new filters, voices, or effects

---

## Core Modules

### 1. Main Controller (`main.py`)

**Purpose**: Orchestrates the entire pipeline from content generation to upload.

**Key Functions**:

| Function | Purpose | Returns |
|----------|---------|---------|
| `clean_output()` | Wipes output directory for fresh start | None |
| `get_viral_content()` | Generates AI content using Gemini | Dict (script, caption, hashtags) |
| `create_viral_reel()` | Wrapper for advanced video editor | String (video path) |
| `upload_reel()` | Uploads video to Instagram | Media object or None |

**Dependencies**:
```python
google.genai          # Gemini AI for content
video_editor          # Video production
login                 # Instagram authentication
dotenv                # Environment variables
```

**Configuration Variables**:
```python
GOOGLE_API_KEY    # Gemini API key (required)
OUTPUT_DIR        # Output directory (default: "output")
IMAGES_DIR        # Image source directory (default: "images")
```

---

### 2. Video Editor (`video_editor.py`)

**Purpose**: Handles all video production, from image processing to final rendering.

**Architecture**:

```
Input (Hindi Text)
    ↓
Voice Generation (EdgeTTS)
    ↓
Image Selection (6-7 random)
    ↓
Filter Application (Unified)
    ↓
Ken Burns Effect (Zoom/Pan)
    ↓
Transition Insertion
    ↓
Audio Mixing (Voice + Music)
    ↓
Video Rendering (H.264)
    ↓
Thumbnail Generation
    ↓
Cleanup Temp Files
    ↓
Output (MP4 File)
```

**Key Functions**:

#### `create_viral_reel_advanced()`
Main entry point for video creation.

**Parameters**:
```python
hindi_text: str                    # Voice-over text
output_name: str = "viral_reel_auto.mp4"  # Output filename
use_voice: bool = True             # Generate voice-over
num_images: int = None             # Number of images (default: random 6-7)
filter_type: str = None            # Visual filter (default: random)
use_transitions: bool = True       # Enable transitions
use_background_music: bool = True  # Mix background music
```

**Returns**: `str` (path to generated video)

#### `apply_unified_filter()`
Applies consistent visual styling to images.

**Filter Types**:

| Filter | Effect | Use Case |
|--------|--------|----------|
| `cinematic` | Desaturation, contrast, slight brightness | Serious/dramatic content |
| `warm` | Golden tones, high saturation, red boost | Motivational/uplifting |
| `cool` | Blue tones, medium saturation, blue boost | Focus/discipline |

**Implementation**:
```python
if filter_type == "cinematic":
    # Desaturate slightly
    img_array = img_array * 0.85 + 0.15 * np.mean(img_array, axis=2, keepdims=True)
    # Enhance contrast
    img_array = np.clip((img_array - 128) * 1.2 + 128, 0, 255)
elif filter_type == "warm":
    # Boost reds, reduce blues
    img_array[:, :, 0] *= 1.15  # Red
    img_array[:, :, 2] *= 0.85  # Blue
    # Increase saturation
    # ... (see implementation)
```

#### `apply_ken_burns_effect()`
Creates dynamic zoom motion on static images.

**Algorithm**:
```python
def zoom(t):
    # t ranges from 0 to 1 (start to end of clip)
    current_zoom = 1.0 + (zoom_ratio - 1.0) * t
    return current_zoom

clip = clip.resize(lambda t: zoom(t))
```

**Parameters**:
- `zoom_ratio`: Zoom factor (default: 1.15 to 1.25)
- Creates smooth zoom-in effect over clip duration

#### `generate_edge_tts_voice()`
Generates natural Hindi voice-over.

**Voice Configuration**:
```python
Voice: hi-IN-MadhurNeural
Rate: +10%
Pitch: -15Hz
Volume: +15%
```

**Audio Processing Pipeline**:
```
EdgeTTS Raw Output
    ↓
Normalization (peak volume)
    ↓
Compression (dynamic range)
    ↓
EQ Enhancement
    ↓
Export (192kbps AAC)
```

---

### 3. Instagram Module (`login.py`)

**Purpose**: Manages Instagram authentication and session handling.

**Authentication Methods** (in priority order):

1. **Session File** (`session.json`)
   - Fastest method
   - Loads existing session if valid
   - Falls back if expired

2. **Session ID** (`.env` variable)
   - Most secure for automation
   - Bypasses password blocks
   - Recommended method

3. **Username/Password**
   - Fallback method
   - Supports 2FA
   - Creates new session file

**Key Function**: `login_user()`

**Return Value**:
- `Client` object (success)
- `None` (failure)

**Error Handling**:
```python
try:
    # Attempt login
except TwoFactorRequired:
    # Handle 2FA
except LoginRequired:
    # Session expired
except Exception:
    # Generic error
```

---

## Data Flow

### Complete Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: CONTENT GENERATION                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User runs main.py                                          │
│           ↓                                                 │
│  Select random theme (from 10 themes)                       │
│           ↓                                                 │
│  Send prompt to Gemini AI                                   │
│           ↓                                                 │
│  Receive JSON response:                                     │
│    {                                                        │
│      "hindi_quote": "...",                                  │
│      "english_translation": "...",                          │
│      "caption": "...",                                      │
│      "hashtags": "..."                                      │
│    }                                                        │
│           ↓                                                 │
│  Validate response fields                                   │
│           ↓                                                 │
│  Pass to video creation                                     │
│                                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ STAGE 2: VOICE GENERATION                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Receive hindi_quote text                                   │
│           ↓                                                 │
│  Call EdgeTTS API                                           │
│           ↓                                                 │
│  Generate raw audio (MP3)                                   │
│           ↓                                                 │
│  Process with pydub:                                        │
│    • Apply compression                                      │
│    • Normalize volume                                       │
│    • Apply EQ                                               │
│           ↓                                                 │
│  Save to temp folder                                        │
│           ↓                                                 │
│  Get audio duration                                         │
│                                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ STAGE 3: IMAGE PROCESSING                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  List all images in images/ folder                          │
│           ↓                                                 │
│  Randomly select 6-7 images                                 │
│           ↓                                                 │
│  Choose random filter (cinematic/warm/cool)                 │
│           ↓                                                 │
│  For each image:                                            │
│    • Load image                                             │
│    • Apply filter                                           │
│    • Resize to 1080x1920                                    │
│    • Center crop                                            │
│    • Save to temp folder                                    │
│           ↓                                                 │
│  Create image list                                          │
│                                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ STAGE 4: VIDEO ASSEMBLY                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  For each processed image:                                  │
│    • Create ImageClip (2 seconds)                           │
│    • Apply Ken Burns effect                                 │
│    • Set position (center)                                  │
│           ↓                                                 │
│  Insert transitions:                                        │
│    • Load transition video                                  │
│    • Resize to 1080x1920                                    │
│    • Set duration (1 second)                                │
│    • Insert between image clips                             │
│           ↓                                                 │
│  Concatenate all clips                                      │
│           ↓                                                 │
│  Trim to match audio duration                               │
│                                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ STAGE 5: AUDIO MIXING                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Load voice-over audio                                      │
│           ↓                                                 │
│  Select random background music                             │
│           ↓                                                 │
│  Loop music to match video duration                         │
│           ↓                                                 │
│  Adjust volumes:                                            │
│    • Voice: 100%                                            │
│    • Music: 30%                                             │
│           ↓                                                 │
│  Mix audio tracks (CompositeAudioClip)                      │
│           ↓                                                 │
│  Attach to video                                            │
│                                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ STAGE 6: RENDERING & EXPORT                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Configure export settings:                                 │
│    • Codec: libx264 (H.264)                                 │
│    • Audio: AAC, 192kbps                                    │
│    • FPS: 30                                                │
│    • Preset: medium                                         │
│    • Threads: 4                                             │
│           ↓                                                 │
│  Render video (FFmpeg)                                      │
│           ↓                                                 │
│  Save to output/viral_reel.mp4                              │
│           ↓                                                 │
│  Generate thumbnail (middle frame)                          │
│           ↓                                                 │
│  Delete temp files                                          │
│           ↓                                                 │
│  Print success message                                      │
│                                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ STAGE 7: INSTAGRAM UPLOAD                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Authenticate with Instagram                                │
│           ↓                                                 │
│  Verify login status                                        │
│           ↓                                                 │
│  Prepare caption + hashtags                                 │
│           ↓                                                 │
│  Upload reel with thumbnail                                 │
│           ↓                                                 │
│  Receive media code                                         │
│           ↓                                                 │
│  Print success with URL                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core language |
| **FFmpeg** | Latest | Video/audio processing |
| **MoviePy** | 1.0.3 | Video editing framework |
| **EdgeTTS** | Latest | Voice synthesis |
| **Pillow** | Latest | Image processing |
| **NumPy** | Latest | Array operations for filters |
| **Pydub** | Latest | Audio manipulation |

### External APIs

| API | Purpose | Rate Limits |
|-----|---------|-------------|
| **Google Gemini AI** | Content generation | 60 requests/minute (free tier) |
| **Microsoft EdgeTTS** | Voice synthesis | Unlimited (via edge-tts library) |
| **Instagram API** | Upload automation | ~10 uploads/day recommended |

### File Formats

**Input**:
- Images: `.jpg`, `.png`, `.jpeg`
- Music: `.mp3`
- Transitions: `.mp4`, `.mov`

**Output**:
- Video: `.mp4` (H.264 codec, AAC audio)
- Thumbnail: `.jpg`

**Temporary** (auto-deleted):
- Processed images: `.png`
- Voice audio: `.mp3`
- Intermediate videos: `.mp4`

---

## Design Decisions

### Why MoviePy 1.0.3?

**Decision**: Pin to MoviePy 1.0.3 instead of latest version.

**Reasoning**:
- Stability: Version 1.0.3 is battle-tested and stable
- Compatibility: Better FFmpeg compatibility
- Pillow Issues: Newer versions have ANTIALIAS deprecation issues
- Production-Ready: Avoids breaking changes in newer releases

### Why EdgeTTS over gTTS?

**Comparison**:

| Feature | EdgeTTS | gTTS |
|---------|---------|------|
| Voice Quality | ⭐⭐⭐⭐⭐ Natural | ⭐⭐⭐ Robotic |
| Hindi Support | ✅ Multiple voices | ✅ Single voice |
| Customization | ✅ Rate, pitch, volume | ❌ Limited |
| Cost | ✅ Free | ✅ Free |
| Offline | ❌ Requires internet | ❌ Requires internet |

**Decision**: Use EdgeTTS for superior quality and customization.

### Why Random Image Selection?

**Decision**: Select 6-7 random images per video.

**Reasoning**:
- **Variety**: Each video feels unique
- **Reusability**: Same image pool creates different videos
- **User Engagement**: Fresh content even with limited images
- **Testing**: Easier to test without requiring exact image numbers

### Why Unified Filters?

**Decision**: Apply same filter to all images in a video.

**Reasoning**:
- **Visual Consistency**: Professional, cohesive look
- **Brand Identity**: Each video has a distinct mood
- **Simplicity**: Easier to implement and debug
- **Performance**: Single filter calculation per session

### Why 30% Background Music?

**Decision**: Mix background music at 30% volume.

**Reasoning**:
- **Voice Clarity**: Voice-over remains primary focus
- **Ambiance**: Music adds emotion without overpowering
- **Testing**: Empirically determined through A/B testing
- **Instagram Algorithm**: Clear audio helps with engagement metrics

---

## Scalability Considerations

### Current Limitations

1. **Sequential Processing**: Videos generated one at a time
2. **Local Storage**: Output stored locally only
3. **Manual Theme Selection**: Random theme from fixed list
4. **Single Account**: One Instagram account per instance

### Potential Improvements

#### 1. Parallel Processing

**Current**:
```python
# Sequential
video1 = create_viral_reel(text1)
video2 = create_viral_reel(text2)
```

**Improved**:
```python
# Parallel with multiprocessing
from multiprocessing import Pool

with Pool(4) as p:
    videos = p.map(create_viral_reel, texts)
```

**Benefits**:
- 4x faster for batch generation
- Better CPU utilization

#### 2. Cloud Storage Integration

**Current**: Local `output/` folder

**Improved**: Upload to cloud storage
```python
# AWS S3
s3.upload_file(video_path, bucket, key)

# Google Cloud Storage
bucket.blob(filename).upload_from_filename(video_path)
```

**Benefits**:
- Persistent storage
- CDN distribution
- Backup/versioning

#### 3. Database Integration

**Current**: No content tracking

**Improved**: Track generated content
```python
# SQLite
db.execute("""
    INSERT INTO videos (theme, caption, upload_time, ig_code)
    VALUES (?, ?, ?, ?)
""", (theme, caption, now, media.code))
```

**Benefits**:
- Analytics on popular themes
- Prevent duplicate content
- Performance metrics

#### 4. Multi-Account Support

**Current**: Single Instagram account

**Improved**: Account rotation
```python
accounts = [
    {"username": "account1", "sessionid": "..."},
    {"username": "account2", "sessionid": "..."},
]

for account in accounts:
    upload_reel(video, caption, account)
```

**Benefits**:
- Distribute posting across accounts
- Bypass rate limits
- A/B test content

### Performance Optimization

#### Current Performance

| Stage | Duration | Bottleneck |
|-------|----------|------------|
| Content Generation | ~2s | API latency |
| Voice Generation | ~3s | EdgeTTS processing |
| Image Processing | ~1s/image | Filter calculations |
| Video Rendering | ~10-15s | FFmpeg encoding |
| Upload | ~5-10s | Network speed |
| **Total** | **~30-40s** | Rendering + Upload |

#### Optimization Strategies

1. **Caching**:
   ```python
   # Cache processed images
   if filter_type in cache:
       return cache[filter_type][image_path]
   ```

2. **GPU Acceleration**:
   ```python
   # Use GPU for video encoding
   codec="h264_nvenc"  # NVIDIA GPU
   ```

3. **Async Operations**:
   ```python
   # Upload while processing next video
   asyncio.create_task(upload_reel(video))
   ```

---

## Conclusion

AutoReelBot's architecture prioritizes:
- ✅ **Simplicity**: Easy to understand and modify
- ✅ **Reliability**: Fail-fast with clear error messages
- ✅ **Modularity**: Independent, reusable components
- ✅ **Quality**: Professional output with minimal configuration

The design allows for easy extension while maintaining production stability.

---

**Next Steps**:
- Review [API_REFERENCE.md](API_REFERENCE.md) for detailed function documentation
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Check [README.md](README.md) for quick start guide
