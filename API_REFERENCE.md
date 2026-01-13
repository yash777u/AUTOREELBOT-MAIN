# 📚 AutoReelBot API Reference

Complete API documentation for all modules and functions in the AutoReelBot system.

## Table of Contents

- [Main Module (main.py)](#main-module-mainpy)
- [Video Editor Module (video_editor.py)](#video-editor-module-video_editorpy)
- [Login Module (login.py)](#login-module-loginpy)
- [Data Structures](#data-structures)
- [Error Handling](#error-handling)
- [Usage Examples](#usage-examples)

---

## Main Module (`main.py`)

### `clean_output()`

Removes and recreates the output directory for a fresh start.

**Signature**:
```python
def clean_output() -> None
```

**Parameters**: None

**Returns**: None

**Side Effects**:
- Deletes `output/` directory and all contents
- Creates fresh `output/` directory
- Creates `images/` directory if missing
- Prints status messages

**Exceptions**:
- Catches `PermissionError` if files are in use (prints warning, continues)

**Example**:
```python
clean_output()
# Output: 🧹 Workspace cleaned.
```

---

### `get_viral_content()`

Generates unique viral content using Google Gemini AI.

**Signature**:
```python
def get_viral_content() -> Dict[str, str]
```

**Parameters**: None

**Returns**: `Dict[str, str]` containing:
```python
{
    "hindi_quote": str,           # 15-20 second Hindi script
    "english_translation": str,   # English translation
    "caption": str,               # SEO-optimized short caption (15-20 words)
    "hashtags": str               # 12-15 trending hashtags
}
```

**Environment Variables**:
- `GOOGLE_API_KEY` (required): Your Gemini API key

**Raises**:
- `ValueError`: If `GOOGLE_API_KEY` is missing
- `RuntimeError`: If Gemini API call fails

**Example**:
```python
content = get_viral_content()
print(content["hindi_quote"])
# Output: "सफलता केवल उन्हें मिलती है जो अपने डर का सामना करते हैं..."
```

**Implementation Details**:

**Themes** (randomly selected):
- Conquering fear and taking action
- Success requires sacrifice
- Being unstoppable in pursuit of goals
- Becoming the best version of yourself
- Discipline over motivation
- Warrior mindset and mental toughness
- Breaking free from average thinking
- Rising after failure
- Dominating your competition
- Building an empire from nothing

**AI Configuration**:
```python
model="gemini-2.5-flash"
temperature=0.9              # High creativity
response_mime_type="application/json"
```

---

### `create_viral_reel()`

Wrapper function for advanced video editor.

**Signature**:
```python
def create_viral_reel(audio_path: Optional[str], hindi_text: str) -> str
```

**Parameters**:
- `audio_path` (str, optional): Path to audio file (ignored, voice generated internally)
- `hindi_text` (str): Hindi text for voice-over generation

**Returns**: `str` - Path to generated video file

**Example**:
```python
video_path = create_viral_reel(None, "मेहनत का फल मीठा होता है")
print(video_path)
# Output: output/viral_reel.mp4
```

**Note**: This is a wrapper around `create_viral_reel_advanced()` with default settings.

---

### `upload_reel()`

Uploads video to Instagram with caption and thumbnail.

**Signature**:
```python
def upload_reel(video_path: str, caption: str) -> Optional[Media]
```

**Parameters**:
- `video_path` (str): Path to video file
- `caption` (str): Caption text including hashtags

**Returns**:
- `Media` object (success)
- `None` (failure)

**Side Effects**:
- Generates thumbnail from video
- Uploads to Instagram
- Prints status messages and URL

**Example**:
```python
caption = "Transform your life! 💪\n\n#motivation #viral #reels"
media = upload_reel("output/viral_reel.mp4", caption)

if media:
    print(f"URL: https://www.instagram.com/reel/{media.code}/")
```

**Error Handling**:

| Error Type | Cause | Suggested Fix |
|------------|-------|---------------|
| `login_required` | Session expired | Get fresh sessionid from browser |
| `challenge` | Verification needed | Complete verification in Instagram app |
| `spam` or `limit` | Posting too fast | Wait 1-2 hours |

---

## Video Editor Module (`video_editor.py`)

### `ensure_directories()`

Creates required directories if they don't exist.

**Signature**:
```python
def ensure_directories() -> None
```

**Creates**:
- `output/`
- `images/`
- `assets/transitions/`
- `assets/background_music/`
- `output/temp/`

**Example**:
```python
ensure_directories()
```

---

### `cleanup_temp_files()`

Deletes all temporary files after video creation.

**Signature**:
```python
def cleanup_temp_files() -> None
```

**Deletes**:
- All files in `output/temp/`
- The `output/temp/` directory itself

**Preserves**:
- Final video in `output/`
- Original images in `images/`

**Example**:
```python
cleanup_temp_files()
# Output: ✅ Cleaned up temp files
```

---

### `generate_edge_tts_voice()`

Generates Hindi voice-over using Microsoft EdgeTTS.

**Signature**:
```python
def generate_edge_tts_voice(
    text: str,
    output_path: str,
    voice_name: str = "hi-IN-MadhurNeural"
) -> None
```

**Parameters**:
- `text` (str): Text to convert to speech
- `output_path` (str): Path to save MP3 file
- `voice_name` (str, optional): EdgeTTS voice name
  - Default: `"hi-IN-MadhurNeural"` (deep male Hindi voice)

**Voice Configuration**:
```python
Rate: +10%      # Slightly faster for engagement
Pitch: -15Hz    # Moderate deepening
Volume: +15%    # Clear and balanced
```

**Raises**:
- `Exception`: If EdgeTTS fails (network issues, invalid voice name)

**Example**:
```python
generate_edge_tts_voice(
    text="सफलता का रहस्य है मेहनत",
    output_path="output/temp/voice.mp3"
)
```

**Available Hindi Voices**:
- `hi-IN-MadhurNeural` (Male, Deep)
- `hi-IN-SwaraNeural` (Female, Clear)

---

### `create_deep_voice_edgetts()`

Wrapper with pydub audio enhancement.

**Signature**:
```python
def create_deep_voice_edgetts(
    text: str,
    output_name: str = "voiceover.mp3"
) -> Tuple[str, float]
```

**Parameters**:
- `text` (str): Text for voice-over
- `output_name` (str, optional): Output filename

**Returns**: `Tuple[str, float]`
- `str`: Path to generated audio file
- `float`: Duration in seconds

**Audio Processing**:
```python
# Compression for consistent volume
compressed = audio.compress_dynamic_range(
    threshold=-20.0,
    ratio=4.0,
    attack=5.0
)

# Normalize to peak volume
normalized = compressed.normalize()

# Optional: Apply EQ boost
```

**Example**:
```python
audio_path, duration = create_deep_voice_edgetts(
    text="आज का दिन है खास",
    output_name="custom_voice.mp3"
)
print(f"Generated: {audio_path} ({duration}s)")
# Output: Generated: output/temp/custom_voice.mp3 (3.5s)
```

---

### `apply_unified_filter()`

Applies consistent visual filter to an image.

**Signature**:
```python
def apply_unified_filter(
    image_path: str,
    filter_type: str = "cinematic"
) -> PIL.Image.Image
```

**Parameters**:
- `image_path` (str): Path to input image
- `filter_type` (str, optional): Filter type
  - `"cinematic"`: Desaturated, high contrast, dramatic
  - `"warm"`: Golden tones, high saturation, uplifting
  - `"cool"`: Blue tones, medium saturation, focused
  - Default: `"cinematic"`

**Returns**: `PIL.Image.Image` - Filtered image (1080x1920, 9:16 ratio)

**Filter Details**:

#### Cinematic Filter
```python
# Desaturation (15%)
# Contrast boost (1.2x)
# Slight brightness increase
# Use case: Serious, dramatic motivational content
```

#### Warm Filter
```python
# Red channel: +15%
# Blue channel: -15%
# Saturation: +30%
# Use case: Uplifting, positive motivational content
```

#### Cool Filter
```python
# Red channel: -15%
# Blue channel: +15%
# Saturation: +20%
# Use case: Focus, discipline, determination content
```

**Example**:
```python
filtered_img = apply_unified_filter("images/warrior.jpg", "cinematic")
filtered_img.save("output/temp/filtered_warrior.png")
```

---

### `apply_ken_burns_effect()`

Applies zoom/pan motion to static image clip.

**Signature**:
```python
def apply_ken_burns_effect(
    clip: ImageClip,
    zoom_ratio: float = 1.2
) -> ImageClip
```

**Parameters**:
- `clip` (ImageClip): MoviePy ImageClip object
- `zoom_ratio` (float, optional): Zoom factor
  - Range: 1.0 to 2.0 recommended
  - Default: 1.2 (20% zoom)

**Returns**: `ImageClip` - Clip with zoom effect applied

**Animation Function**:
```python
def zoom(t):
    # t = 0 at start, t = 1 at end
    return 1.0 + (zoom_ratio - 1.0) * t

# At t=0: zoom = 1.0 (original size)
# At t=1: zoom = zoom_ratio (fully zoomed)
```

**Example**:
```python
from moviepy.editor import ImageClip

img_clip = ImageClip("images/mountain.jpg", duration=2)
animated_clip = apply_ken_burns_effect(img_clip, zoom_ratio=1.25)
```

**Visual Effect**:
```
Time 0s: [████████████] (100% size)
Time 1s: [█████████████] (112.5% size)
Time 2s: [██████████████] (125% size)
```

---

### `create_viral_reel_advanced()`

Main function for creating complete viral reel with all effects.

**Signature**:
```python
def create_viral_reel_advanced(
    hindi_text: str,
    output_name: str = "viral_reel_auto.mp4",
    use_voice: bool = True,
    num_images: Optional[int] = None,
    filter_type: Optional[str] = None,
    use_transitions: bool = True,
    use_background_music: bool = True
) -> str
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hindi_text` | `str` | *required* | Hindi text for voice-over |
| `output_name` | `str` | `"viral_reel_auto.mp4"` | Output filename |
| `use_voice` | `bool` | `True` | Generate voice-over |
| `num_images` | `int` | `None` | Number of images (None = random 6-7) |
| `filter_type` | `str` | `None` | Filter type (None = random) |
| `use_transitions` | `bool` | `True` | Add transition effects |
| `use_background_music` | `bool` | `True` | Mix background music |

**Returns**: `str` - Path to generated video

**Process**:
1. Generate voice-over (if `use_voice=True`)
2. Select images (random or specified count)
3. Choose filter (random or specified)
4. Process images with filter
5. Create clips with Ken Burns effect (2 seconds each)
6. Insert transitions (1 second each)
7. Concatenate clips
8. Mix audio (voice + music)
9. Render final video
10. Cleanup temp files

**Export Settings**:
```python
codec="libx264"           # H.264 video
audio_codec="aac"         # AAC audio
fps=30                    # 30 frames per second
preset="medium"           # Encoding speed/quality balance
audio_bitrate="192k"      # High-quality audio
threads=4                 # Parallel encoding
```

**Example 1: Basic Usage**
```python
video = create_viral_reel_advanced(
    hindi_text="जीत हमारी होगी"
)
# Creates video with all default settings
```

**Example 2: Custom Configuration**
```python
video = create_viral_reel_advanced(
    hindi_text="संघर्ष ही जीवन है",
    output_name="custom_reel.mp4",
    num_images=5,
    filter_type="warm",
    use_transitions=False,
    use_background_music=False
)
# Custom video: 5 images, warm filter, no transitions/music
```

**Example 3: Silent Video**
```python
video = create_viral_reel_advanced(
    hindi_text="",
    use_voice=False,
    num_images=8
)
# Silent video with 8 images
```

**Output Structure**:
```
output/
├── viral_reel_auto.mp4  # Final video
└── temp/                # Auto-deleted after creation
    ├── voiceover.mp3
    ├── filtered_image_0.png
    ├── filtered_image_1.png
    └── ...
```

**Success Message**:
```
🎉 SUCCESS! ENHANCED VIRAL REEL CREATED!
============================================================
📹 File: output/viral_reel_auto.mp4
⏱️  Duration: 18.0s
🖼️  Images: 7 (2.0s each)
🎨 Filter: cinematic
⚡ Motion: Ken Burns effect (1.2x zoom)
🎬 Transitions: 6
🎙️ Voice: Natural Hindi (hi-IN-MadhurNeural)
🎵 Music: epic_background.mp3 (30% volume)
💾 File size: 18.3 MB
✨ Output: Clean (temp files deleted)
============================================================
```

---

### `generate_thumbnail()`

Extracts middle frame from video as thumbnail.

**Signature**:
```python
def generate_thumbnail(video_path: str) -> str
```

**Parameters**:
- `video_path` (str): Path to video file

**Returns**: `str` - Path to generated thumbnail JPG

**Implementation**:
```python
# Load video
clip = VideoFileClip(video_path)

# Get middle frame (t = duration / 2)
frame = clip.get_frame(clip.duration / 2)

# Save as JPEG
thumbnail_path = video_path.replace('.mp4', '_thumbnail.jpg')
```

**Example**:
```python
thumb = generate_thumbnail("output/viral_reel.mp4")
print(thumb)
# Output: output/viral_reel_thumbnail.jpg
```

---

## Login Module (`login.py`)

### `login_user()`

Authenticates with Instagram using multiple methods.

**Signature**:
```python
def login_user() -> Optional[Client]
```

**Parameters**: None

**Returns**:
- `Client` object (success)
- `None` (failure)

**Environment Variables**:
- `INSTA_USERNAME` (optional): Instagram username
- `INSTA_PASSWORD` (optional): Instagram password
- `INSTA_SESSIONID` (optional): Session ID from browser cookies

**Authentication Hierarchy**:

```
1. Try session.json file
   ↓ (if invalid)
2. Try INSTA_SESSIONID from .env
   ↓ (if missing/invalid)
3. Try USERNAME + PASSWORD
   ↓ (if 2FA required)
4. Prompt for 2FA code
```

**Example**:
```python
client = login_user()

if client:
    user = client.account_info()
    print(f"Logged in as: {user.username}")
else:
    print("Login failed")
```

**Session Management**:

**Creating `session.json`**:
```python
# First login creates session.json automatically
client = login_user()
# session.json is saved for future use
```

**Reusing Session**:
```python
# Subsequent runs load session.json
client = login_user()
# No password needed, instant login
```

**Getting Session ID from Browser**:
1. Open Instagram in browser (logged in)
2. Press `F12` (DevTools)
3. Go to **Application** → **Cookies** → `https://www.instagram.com`
4. Copy value of `sessionid` cookie
5. Add to `.env`: `INSTA_SESSIONID=your_session_id_here`

---

## Data Structures

### Gemini AI Response

```python
{
    "hindi_quote": str,
    # Example: "सफलता का रहस्य है निरंतर प्रयास..."
    # Length: ~15-20 seconds when spoken
    
    "english_translation": str,
    # Example: "The secret to success is continuous effort..."
    # Provided for reference only
    
    "caption": str,
    # Example: "Transform your mindset, transform your life! 💪"
    # Length: 15-20 words
    # SEO-optimized for Instagram
    
    "hashtags": str
    # Example: "#motivation #success #viral #reels #hindi #inspiration..."
    # Count: 12-15 hashtags
    # Mix of trending and niche tags
}
```

### Video Metadata

```python
{
    "file_path": str,           # output/viral_reel.mp4
    "duration": float,          # 18.5 (seconds)
    "num_images": int,          # 7
    "filter_type": str,         # "cinematic"
    "num_transitions": int,     # 6
    "has_voice": bool,          # True
    "has_music": bool,          # True
    "file_size_mb": float,      # 20.6
    "resolution": tuple,        # (1080, 1920)
    "fps": int,                 # 30
    "codec": str               # "libx264"
}
```

### Instagram Media Object

```python
Media(
    code="ABC123xyz",          # Reel code
    id="1234567890",           # Media ID
    taken_at=datetime,         # Upload timestamp
    caption_text=str,          # Caption
    user=User(...),            # Your account info
    # ... (see instagrapi docs for full structure)
)
```

---

## Error Handling

### Exception Types

#### Content Generation Errors

```python
try:
    content = get_viral_content()
except ValueError as e:
    # Missing GOOGLE_API_KEY
    print(f"Configuration error: {e}")
except RuntimeError as e:
    # Gemini API failure
    print(f"AI service error: {e}")
```

#### Video Creation Errors

```python
try:
    video = create_viral_reel_advanced(text)
except FileNotFoundError:
    # No images in images/ folder
    print("Add at least 6 images to images/ folder")
except Exception as e:
    # FFmpeg error, memory issue, etc.
    print(f"Video creation failed: {e}")
```

#### Instagram Upload Errors

```python
try:
    upload_reel(video, caption)
except LoginRequired:
    # Session expired
    print("Get fresh sessionid from browser")
except ChallengeRequired:
    # Verification needed
    print("Complete verification in Instagram app")
except TwoFactorRequired:
    # 2FA code needed
    code = input("Enter 2FA code: ")
    client.two_factor_login(code)
```

### Error Recovery

**Gemini API Rate Limit**:
```python
# Wait and retry
import time
for attempt in range(3):
    try:
        content = get_viral_content()
        break
    except RuntimeError as e:
        if "rate limit" in str(e).lower():
            time.sleep(60)  # Wait 1 minute
        else:
            raise
```

**Instagram Upload Failure**:
```python
# Video is saved even if upload fails
if not upload_reel(video, caption):
    print(f"Upload failed, but video saved at: {video}")
    print("You can manually upload or retry later")
```

---

## Usage Examples

### Example 1: Basic Automation

```python
from main import clean_output, get_viral_content, create_viral_reel, upload_reel

# Clean workspace
clean_output()

# Generate content
content = get_viral_content()
print(f"Generated: {content['hindi_quote'][:50]}...")

# Create video
video = create_viral_reel(None, content['hindi_quote'])
print(f"Video created: {video}")

# Upload
caption = f"{content['caption']}\n\n{content['hashtags']}"
media = upload_reel(video, caption)

if media:
    print(f"Success! https://www.instagram.com/reel/{media.code}/")
```

### Example 2: Custom Video Creation

```python
from video_editor import create_viral_reel_advanced

# Cinematic video with 5 images, no music
video = create_viral_reel_advanced(
    hindi_text="जीवन एक संघर्ष है, इसे स्वीकार करो",
    output_name="cinematic_reel.mp4",
    num_images=5,
    filter_type="cinematic",
    use_transitions=True,
    use_background_music=False
)

print(f"Created: {video}")
```

### Example 3: Batch Video Generation

```python
themes = [
    "सफलता का मंत्र",
    "योद्धा मानसिकता",
    "अनुशासन की शक्ति"
]

for i, theme in enumerate(themes):
    content = get_viral_content()
    video = create_viral_reel_advanced(
        hindi_text=content['hindi_quote'],
        output_name=f"reel_{i+1}.mp4"
    )
    print(f"Created video {i+1}: {video}")
```

### Example 4: Testing Without Upload

```python
# Create video without uploading
content = get_viral_content()
video = create_viral_reel(None, content['hindi_quote'])

# Just save locally
print(f"Video ready at: {video}")
print("Upload manually when ready")
```

### Example 5: Custom Audio and Images

```python
# Specific number of images with warm filter
video = create_viral_reel_advanced(
    hindi_text="आज का दिन खास बनाओ",
    output_name="warm_motivational.mp4",
    num_images=8,
    filter_type="warm",
    use_voice=True,
    use_background_music=True
)
```

### Example 6: Error Handling

```python
import sys

try:
    # Full pipeline
    clean_output()
    content = get_viral_content()
    video = create_viral_reel(None, content['hindi_quote'])
    caption = f"{content['caption']}\n\n{content['hashtags']}"
    upload_reel(video, caption)
    
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    print("💡 Check your .env file")
    sys.exit(1)
    
except RuntimeError as e:
    print(f"❌ AI service error: {e}")
    print("💡 Check your GOOGLE_API_KEY")
    sys.exit(1)
    
except FileNotFoundError:
    print("❌ No images found")
    print("💡 Add images to images/ folder")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
```

---

## Performance Notes

### Memory Usage

| Operation | RAM Usage | Notes |
|-----------|-----------|-------|
| Content Generation | ~50 MB | Gemini API minimal |
| Voice Generation | ~100 MB | EdgeTTS processing |
| Image Processing | ~200 MB per image | Filter calculations |
| Video Rendering | ~500 MB - 1 GB | FFmpeg buffer |
| **Peak Usage** | **~1.5 GB** | During rendering |

### Execution Time

| Stage | Duration | Optimization |
|-------|----------|--------------|
| Content Gen | 1-3s | API latency, can't optimize |
| Voice Gen | 2-4s | Network dependent |
| Image Processing | 0.5s/image | Use caching for repeated images |
| Video Rendering | 10-20s | Use GPU encoding if available |
| Upload | 5-15s | Network dependent |
| **Total** | **30-60s** | Mostly rendering + upload |

### Optimization Tips

1. **GPU Acceleration**:
   ```python
   # In create_viral_reel_advanced(), change codec:
   codec="h264_nvenc"  # NVIDIA GPU
   codec="h264_videotoolbox"  # macOS
   ```

2. **Reduce Resolution**:
   ```python
   # Lower quality for faster processing
   TARGET_SIZE = (720, 1280)  # Instead of (1080, 1920)
   ```

3. **Disable Effects**:
   ```python
   # Skip transitions for faster creation
   create_viral_reel_advanced(
       text="...",
       use_transitions=False
   )
   ```

---

## Version Compatibility

| Component | Tested Version | Notes |
|-----------|---------------|-------|
| Python | 3.8, 3.9, 3.10, 3.11 | 3.8+ required |
| MoviePy | 1.0.3 | **Pin to 1.0.3** (stability) |
| FFmpeg | 4.x, 5.x, 6.x | Any recent version |
| Pillow | 9.x, 10.x | 10.x requires ANTIALIAS fix |
| EdgeTTS | Latest | Auto-updated |

**Critical**: Keep MoviePy at 1.0.3 for stability.

---

For more information:
- [README.md](README.md) - Quick start guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
