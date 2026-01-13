# 🔧 AutoReelBot Troubleshooting Guide

Complete troubleshooting guide for common issues and their solutions.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Content Generation Issues](#content-generation-issues)
- [Voice Generation Issues](#voice-generation-issues)
- [Video Creation Issues](#video-creation-issues)
- [Instagram Upload Issues](#instagram-upload-issues)
- [Performance Issues](#performance-issues)
- [Environment & Configuration](#environment--configuration)
- [FAQ](#faq)

---

## Installation Issues

### ❌ `ModuleNotFoundError: No module named 'moviepy'`

**Cause**: Dependencies not installed or virtual environment not activated.

**Solution 1**: Install dependencies
```bash
pip install -r requirements.txt
```

**Solution 2**: Verify virtual environment
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Then install again
pip install -r requirements.txt
```

**Solution 3**: Upgrade pip
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### ❌ `FileNotFoundError: [WinError 2] The system cannot find the file specified: 'ffmpeg'`

**Cause**: FFmpeg not installed or not in system PATH.

**Solution (Windows)**:

1. Download FFmpeg:
   - Visit [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Download Windows build (essentials)

2. Extract to `C:\ffmpeg`

3. Add to PATH:
   ```
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Edit "Path" → New → Add: C:\ffmpeg\bin
   - Click OK on all dialogs
   - **RESTART YOUR TERMINAL**
   ```

4. Verify installation:
   ```bash
   ffmpeg -version
   ```

**Solution (Linux)**:
```bash
sudo apt update
sudo apt install ffmpeg -y
ffmpeg -version
```

**Solution (macOS)**:
```bash
brew install ffmpeg
ffmpeg -version
```

**Still not working?**
```bash
# Find FFmpeg location
# Windows
where ffmpeg

# Linux/Mac
which ffmpeg

# If found, add that directory to PATH
```

---

### ❌ `AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'`

**Cause**: Pillow 10+ deprecated `ANTIALIAS` constant.

**Solution**: The fix is already in `main.py` (lines 8-11):
```python
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
```

If error persists:
```bash
# Downgrade Pillow
pip install Pillow==9.5.0
```

---

### ❌ `ERROR: Could not build wheels for moviepy`

**Cause**: Compilation issues with MoviePy dependencies.

**Solution**:
```bash
# Install pre-built binaries
pip install --only-binary :all: moviepy==1.0.3

# If that fails, install build tools:
# Windows: Install Visual Studio Build Tools
# Linux: sudo apt install build-essential python3-dev
# Mac: xcode-select --install

# Then retry
pip install moviepy==1.0.3
```

---

## Content Generation Issues

### ❌ `ValueError: ❌ GOOGLE_API_KEY missing in .env file!`

**Cause**: Missing or incorrect Google Gemini API key.

**Solution**:

1. **Get API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Click "Create API Key"
   - Copy the key

2. **Create/Edit `.env` file**:
   ```env
   GOOGLE_API_KEY=AIzaSyC_your_actual_api_key_here
   ```

3. **Verify `.env` location**:
   - Must be in project root directory (same folder as `main.py`)
   - Check filename is exactly `.env` (not `env.txt` or `.env.txt`)

4. **Test**:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   print(os.getenv("GOOGLE_API_KEY"))
   # Should print your key
   ```

---

### ❌ `RuntimeError: Failed to generate content from Gemini: 429`

**Cause**: Gemini API rate limit exceeded.

**Solution**:

1. **Check quota**:
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Check "Quota" section

2. **Wait and retry**:
   ```bash
   # Free tier limits:
   # - 60 requests per minute
   # - 1500 requests per day
   
   # Wait 1 minute and try again
   ```

3. **Implement retry logic** (add to `main.py`):
   ```python
   import time
   
   for attempt in range(3):
       try:
           content = get_viral_content()
           break
       except RuntimeError as e:
           if "429" in str(e):
               wait_time = (attempt + 1) * 60
               print(f"Rate limit hit, waiting {wait_time}s...")
               time.sleep(wait_time)
           else:
               raise
   ```

---

### ❌ `RuntimeError: Failed to generate content from Gemini: 400 Bad Request`

**Cause**: Invalid API request or malformed prompt.

**Solutions**:

1. **Verify API key**:
   ```bash
   # Test API key directly
   curl "https://generativelanguage.googleapis.com/v1/models?key=YOUR_API_KEY"
   ```

2. **Check Gemini model availability**:
   - Model `gemini-2.5-flash` may not be available in your region
   - Try changing model in `main.py`:
   ```python
   # In get_viral_content():
   response = client.models.generate_content(
       model="gemini-1.5-flash",  # Changed from gemini-2.5-flash
       # ... rest of code
   )
   ```

3. **Reduce prompt complexity**:
   - Simplify the prompt if it's too long
   - Remove special characters

---

### ❌ `ValueError: ❌ Gemini response missing required fields!`

**Cause**: Gemini returned incomplete JSON.

**Solution**:

1. **Check actual response**:
   Add debug logging to `get_viral_content()`:
   ```python
   import json
   
   # After response = client.models.generate_content(...)
   print("Raw response:", response.text)
   content = json.loads(response.text)
   print("Parsed content:", content)
   ```

2. **Lower temperature**:
   ```python
   config=types.GenerateContentConfig(
       response_mime_type="application/json",
       temperature=0.7  # Changed from 0.9 for more consistent output
   )
   ```

3. **Provide fallback**:
   ```python
   # Add default values
   content.setdefault("hindi_quote", "Default Hindi text")
   content.setdefault("caption", "Default caption")
   content.setdefault("hashtags", "#motivation #viral")
   ```

---

## Voice Generation Issues

### ❌ `Exception: Voice generation failed with EdgeTTS`

**Cause**: Network issues, invalid voice name, or EdgeTTS service down.

**Solutions**:

1. **Check internet connection**:
   ```bash
   ping microsoft.com
   # EdgeTTS requires internet access
   ```

2. **Update edge-tts**:
   ```bash
   pip install edge-tts --upgrade
   ```

3. **Test EdgeTTS directly**:
   ```bash
   # List available voices
   edge-tts --list-voices | grep hi-IN
   
   # Test voice generation
   edge-tts --text "यह एक परीक्षण है" --voice hi-IN-MadhurNeural --write-media test.mp3
   ```

4. **Try alternative voice**:
   ```python
   # In video_editor.py, change voice name:
   generate_edge_tts_voice(
       text=text,
       output_path=output_path,
       voice_name="hi-IN-SwaraNeural"  # Female voice
   )
   ```

5. **Fallback to gTTS**:
   ```python
   # Install gTTS
   pip install gTTS
   
   # Replace EdgeTTS with gTTS
   from gtts import gTTS
   
   def generate_gtts_voice(text, output_path):
       tts = gTTS(text=text, lang='hi')
       tts.save(output_path)
   ```

---

### ❌ Voice sounds robotic or unnatural

**Cause**: Suboptimal EdgeTTS parameters or voice choice.

**Solutions**:

1. **Adjust voice parameters** in `video_editor.py`:
   ```python
   # Try different combinations:
   
   # More natural (slower, less pitch change)
   rate="+0%"
   pitch="-5Hz"
   volume="+10%"
   
   # Deeper, more masculine
   rate="+5%"
   pitch="-25Hz"
   volume="+20%"
   
   # Faster, energetic
   rate="+20%"
   pitch="-10Hz"
   volume="+15%"
   ```

2. **Try different voice**:
   ```bash
   # List all Hindi voices
   edge-tts --list-voices | grep hi-IN
   
   # Available voices:
   # hi-IN-MadhurNeural (Male, Deep)
   # hi-IN-SwaraNeural (Female, Clear)
   ```

3. **Improve text formatting**:
   ```python
   # Add pauses with commas
   "सफलता का रहस्य, निरंतर प्रयास है।"  # Better
   "सफलता का रहस्य निरंतर प्रयास है"   # Worse
   ```

---

### ❌ `ModuleNotFoundError: No module named 'pydub'`

**Cause**: Pydub not installed for audio processing.

**Solution**:
```bash
pip install pydub
```

If audio processing still fails:
```bash
# Pydub requires FFmpeg
# Verify FFmpeg is installed:
ffmpeg -version

# If not, install FFmpeg (see FFmpeg section above)
```

---

## Video Creation Issues

### ❌ `FileNotFoundError: No images found in images/ folder`

**Cause**: No images in the `images/` directory.

**Solution**:

1. **Add images**:
   ```bash
   # Create images folder
   mkdir images
   
   # Add at least 6 images (JPG, PNG, JPEG)
   # Copy your motivational/warrior images to this folder
   ```

2. **Check image formats**:
   ```python
   # Supported formats
   ['.jpg', '.jpeg', '.png']
   
   # NOT supported
   ['.gif', '.bmp', '.webp', '.tiff']
   ```

3. **Verify with script**:
   ```python
   import os
   
   images = [f for f in os.listdir('images') 
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
   print(f"Found {len(images)} images:")
   for img in images:
       print(f"  - {img}")
   ```

---

### ❌ `OSError: [Errno 28] No space left on device`

**Cause**: Insufficient disk space for video rendering.

**Solution**:

1. **Check disk space**:
   ```bash
   # Windows
   wmic logicaldisk get size,freespace,caption
   
   # Linux/Mac
   df -h
   ```

2. **Clean temp files**:
   ```bash
   # Delete output folder
   rm -rf output/
   
   # Clear Python cache
   find . -type d -name __pycache__ -exec rm -rf {} +
   ```

3. **Free up space**:
   - Need at least **500 MB** free for video creation
   - Delete old videos from `output/` folder
   - Clear system temp files

---

### ❌ Video export hangs or takes forever

**Cause**: FFmpeg encoding issues, large files, or slow hardware.

**Solutions**:

1. **Check FFmpeg process**:
   ```bash
   # Windows
   tasklist | findstr ffmpeg
   
   # Linux/Mac
   ps aux | grep ffmpeg
   
   # If stuck, kill process:
   taskkill /F /IM ffmpeg.exe  # Windows
   killall ffmpeg              # Linux/Mac
   ```

2. **Reduce video quality** in `video_editor.py`:
   ```python
   # In create_viral_reel_advanced():
   final_video.write_videofile(
       output_path,
       codec="libx264",
       fps=24,              # Changed from 30
       preset="ultrafast",  # Changed from "medium"
       threads=2,           # Changed from 4 if low CPU
       # ... rest
   )
   ```

3. **Lower resolution**:
   ```python
   # In apply_unified_filter():
   TARGET_SIZE = (720, 1280)  # Instead of (1080, 1920)
   ```

4. **Disable transitions**:
   ```python
   video = create_viral_reel_advanced(
       hindi_text=text,
       use_transitions=False  # Faster rendering
   )
   ```

---

### ❌ `RuntimeError: FFMPEG encountered the following error while writing file`

**Cause**: Corrupted video, codec issues, or file permissions.

**Solutions**:

1. **Check output folder permissions**:
   ```bash
   # Windows: Run as Administrator
   # Linux/Mac:
   chmod 777 output/
   ```

2. **Try different codec**:
   ```python
   # In video_editor.py:
   codec="mpeg4"  # Instead of libx264
   ```

3. **Verify FFmpeg codecs**:
   ```bash
   ffmpeg -codecs | grep h264
   # Should show libx264 encoder
   
   # If missing, reinstall FFmpeg
   ```

4. **Check file path length**:
   ```python
   # Keep output paths short
   # BAD:  "C:/Very/Long/Path/With/Many/Folders/output.mp4"
   # GOOD: "output/viral_reel.mp4"
   ```

---

### ❌ Transitions not loading or causing errors

**Cause**: Missing transitions folder or incompatible transition files.

**Solutions**:

1. **Create transitions folder**:
   ```bash
   mkdir -p assets/transitions
   ```

2. **Add transition files**:
   - Use `.mp4` or `.mov` files
   - Duration: 1-2 seconds
   - Resolution: Any (will be resized automatically)

3. **Disable transitions if not needed**:
   ```python
   video = create_viral_reel_advanced(
       hindi_text=text,
       use_transitions=False
   )
   ```

4. **Check transition file format**:
   ```python
   import os
   
   transitions = [f for f in os.listdir('assets/transitions')
                  if f.lower().endswith(('.mp4', '.mov'))]
   print(f"Found {len(transitions)} transitions")
   ```

---

### ❌ Background music not playing or causing errors

**Cause**: Missing music folder or incompatible audio files.

**Solutions**:

1. **Create music folder**:
   ```bash
   mkdir -p assets/background_music
   ```

2. **Add music files**:
   - Use `.mp3` format only
   - Any duration (will be looped)
   - Use copyright-free music

3. **Disable music if not needed**:
   ```python
   video = create_viral_reel_advanced(
       hindi_text=text,
       use_background_music=False
   )
   ```

4. **Test audio file**:
   ```bash
   ffmpeg -i assets/background_music/your_music.mp3
   # Should show audio info without errors
   ```

---

## Instagram Upload Issues

### ❌ `login_required` error

**Cause**: Instagram session expired or invalid.

**Solution**:

**Method 1: Get fresh Session ID** (Recommended)

1. Open Instagram in browser (logged in)
2. Press `F12` (DevTools)
3. Go to **Application** → **Cookies** → `https://www.instagram.com`
4. Find `sessionid` cookie
5. Copy its **Value**
6. Update `.env`:
   ```env
   INSTA_SESSIONID=paste_value_here
   ```
7. Delete old `session.json`:
   ```bash
   rm session.json  # Linux/Mac
   del session.json  # Windows
   ```
8. Run script again

**Method 2: Fresh login**
1. Delete `session.json`
2. Remove `INSTA_SESSIONID` from `.env`
3. Add credentials to `.env`:
   ```env
   INSTA_USERNAME=your_username
   INSTA_PASSWORD=your_password
   ```
4. Run script - it will create new session

---

### ❌ `challenge_required` error

**Cause**: Instagram requires verification (suspicious activity).

**Solution**:

1. **Complete verification**:
   - Open Instagram app on phone
   - Complete any verification challenges
   - Verify it's you (email code, SMS, etc.)

2. **Wait and retry**:
   - Wait 1-2 hours
   - Instagram may auto-clear the challenge

3. **Use different network**:
   - Try different WiFi network
   - Or use mobile hotspot
   - Sometimes IP-based restriction

4. **Get new session ID**:
   - After completing verification in browser
   - Get fresh sessionid from browser cookies
   - Update `.env`

---

### ❌ `spam` or `limit` error

**Cause**: Posting too frequently, Instagram rate limit.

**Solution**:

1. **Wait**:
   - Wait at least 30 minutes between uploads
   - Don't upload more than 10 videos per day

2. **Vary posting behavior**:
   - Post at different times
   - Add variety to captions
   - Use different images

3. **Check account status**:
   - Open Instagram app
   - Check for warnings or restrictions
   - Review Community Guidelines

---

### ❌ Upload succeeds but returns `None` or pydantic error

**Cause**: Instagrapi parsing error (non-critical).

**Solution**:

This is often a **false error** - the video may have uploaded successfully!

1. **Check your profile**:
   ```
   https://www.instagram.com/your_username/
   ```
   See if the reel appears

2. **Ignore pydantic errors**:
   Already handled in `main.py`:
   ```python
   if "pydantic" in error_str.lower():
       print("Upload likely SUCCEEDED (pydantic parsing error)")
   ```

3. **Update instagrapi**:
   ```bash
   pip install instagrapi --upgrade
   ```

---

### ❌ `TwoFactorRequired` error

**Cause**: 2FA enabled on Instagram account.

**Solution**:

The script handles this automatically:
```python
except TwoFactorRequired:
    print("📱 2FA Required!")
    code = input("Enter 2FA Code: ")
    cl.two_factor_login(code)
```

Just enter the 6-digit code when prompted.

**To avoid 2FA prompts**:
1. Complete 2FA once
2. session.json will be saved
3. Future runs won't need 2FA

---

## Performance Issues

### ❌ Script runs too slowly

**Cause**: Slow hardware, large files, or unoptimized settings.

**Solutions**:

1. **Use GPU encoding** (if you have NVIDIA GPU):
   ```python
   # In video_editor.py:
   codec="h264_nvenc"  # Instead of libx264
   ```

2. **Reduce image count**:
   ```python
   video = create_viral_reel_advanced(
       hindi_text=text,
       num_images=5  # Instead of 6-7
   )
   ```

3. **Lower FPS**:
   ```python
   fps=24  # Instead of 30
   ```

4. **Use faster preset**:
   ```python
   preset="fast"  # Instead of "medium"
   # Options: ultrafast, superfast, veryfast, faster, fast, medium, slow
   ```

5. **Disable effects temporarily**:
   ```python
   video = create_viral_reel_advanced(
       hindi_text=text,
       use_transitions=False,
       use_background_music=False
   )
   ```

---

### ❌ High memory usage or out of memory errors

**Cause**: Processing large images or long videos.

**Solutions**:

1. **Reduce image resolution**:
   ```python
   # Before processing, resize images:
   from PIL import Image
   
   img = Image.open('image.jpg')
   img = img.resize((1080, 1080))  # Smaller than full 1080x1920
   ```

2. **Process images in batches**:
   ```python
   # Instead of all at once
   for img_path in image_paths:
       process_image(img_path)
       # Clear memory
       import gc
       gc.collect()
   ```

3. **Increase virtual memory**:
   - Windows: System → Advanced → Performance → Settings → Advanced → Virtual Memory
   - Increase page file size

4. **Close other applications**:
   - Close browser, other programs
   - Free up RAM

---

## Environment & Configuration

### ❌ `.env` file not loading

**Cause**: Wrong filename, location, or encoding.

**Solutions**:

1. **Verify filename**:
   ```bash
   # File should be named exactly:
   .env
   
   # NOT:
   env.txt
   .env.txt
   env
   ```

2. **Verify location**:
   ```
   AutoReelBot/
   ├── .env          ← Should be here
   ├── main.py
   ├── video_editor.py
   └── ...
   ```

3. **Check encoding**:
   - Save as UTF-8 (no BOM)
   - No extra spaces or quotes:
   ```env
   # CORRECT
   GOOGLE_API_KEY=AIzaSyC...
   
   # WRONG
   GOOGLE_API_KEY = "AIzaSyC..."
   GOOGLE_API_KEY='AIzaSyC...'
   ```

4. **Test loading**:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   print("API Key:", os.getenv("GOOGLE_API_KEY"))
   print("Username:", os.getenv("INSTA_USERNAME"))
   ```

---

### ❌ Virtual environment not activating

**Cause**: Wrong activation command or path issues.

**Solutions**:

**Windows (PowerShell)**:
```powershell
# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**:
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac**:
```bash
source venv/bin/activate
```

**Verify activation**:
```bash
# Should show (venv) prefix:
(venv) C:\AutoReelBot>

# Check Python path:
which python  # Linux/Mac
where python  # Windows
# Should point to venv/bin/python or venv\Scripts\python.exe
```

---

## FAQ

### Q: How many videos can I generate per day?

**A**: No technical limit, but Instagram recommends:
- **10-15 uploads per day maximum**
- **30+ minutes between uploads**
- More can trigger spam detection

### Q: Can I use my own voice-over files?

**A**: Yes! Modify `create_viral_reel_advanced()`:
```python
# Skip voice generation
video = create_viral_reel_advanced(
    hindi_text="",
    use_voice=False
)

# Then manually add your audio:
from moviepy.editor import VideoFileClip, AudioFileClip

video = VideoFileClip("output/viral_reel.mp4")
audio = AudioFileClip("my_voiceover.mp3")
final = video.set_audio(audio)
final.write_videofile("output/final.mp4")
```

### Q: Can I change video resolution?

**A**: Yes, modify `TARGET_SIZE` in `video_editor.py`:
```python
# For 9:16 format:
TARGET_SIZE = (1080, 1920)  # Full HD (default)
TARGET_SIZE = (720, 1280)   # HD
TARGET_SIZE = (540, 960)    # SD

# For other formats:
TARGET_SIZE = (1920, 1080)  # 16:9 landscape
TARGET_SIZE = (1080, 1080)  # 1:1 square
```

### Q: How do I use custom fonts in videos?

**A**: MoviePy supports text overlays:
```python
from moviepy.editor import TextClip

txt = TextClip(
    "Your Text",
    fontsize=70,
    color='white',
    font='Arial-Bold'  # Or path to TTF file
)
txt = txt.set_position('center').set_duration(5)

# Overlay on video
final = CompositeVideoClip([video, txt])
```

### Q: Can I schedule automatic posting?

**A**: Yes! Use Windows Task Scheduler or cron:

**Windows Task Scheduler**:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at specific time
4. Action: Start a program
5. Program: `C:\Path\To\venv\Scripts\python.exe`
6. Arguments: `C:\Path\To\main.py`

**Linux cron**:
```bash
# Edit crontab
crontab -e

# Add line (posts at 9 AM daily):
0 9 * * * cd /path/to/AutoReelBot && /path/to/venv/bin/python main.py
```

### Q: How do I add watermarks?

**A**: Use CompositeVideoClip:
```python
from moviepy.editor import ImageClip, CompositeVideoClip

# Load watermark
watermark = (ImageClip("watermark.png")
    .set_duration(video.duration)
    .resize(height=50)
    .set_position(("right", "bottom"))
    .set_opacity(0.5))

# Overlay on video
final = CompositeVideoClip([video, watermark])
```

### Q: Can I use this for other languages?

**A**: Yes! Change voice in `video_editor.py`:
```python
# English
voice_name="en-US-GuyNeural"

# Spanish
voice_name="es-ES-AlvaroNeural"

# List all voices:
# edge-tts --list-voices
```

And modify Gemini prompt in `main.py` for content in your language.

### Q: Video quality looks poor on Instagram

**A**: Instagram compresses videos. To improve:
```python
# In video_editor.py:

# Higher bitrate
bitrate="5000k"  # Instead of default

# Better audio
audio_bitrate="256k"  # Instead of 192k

# Use Instagram-optimal settings
fps=30
codec="libx264"
preset="slow"  # Better quality, slower encoding
```

---

## Getting Help

If your issue isn't covered here:

1. **Check logs**: Look for specific error messages in terminal output

2. **Search issues**: Check [GitHub Issues](https://github.com/yourusername/AutoReelBot/issues)

3. **Create issue**: If problem persists, create detailed issue with:
   - Error message (full traceback)
   - Python version: `python --version`
   - OS and version
   - What you've already tried

4. **Community**: Join discussions at [GitHub Discussions](https://github.com/yourusername/AutoReelBot/discussions)

---

## Still Having Issues?

**Debug Checklist**:

- [ ] Python 3.8+ installed
- [ ] FFmpeg installed and in PATH
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file exists with correct keys
- [ ] At least 6 images in `images/` folder
- [ ] Internet connection active (for Gemini, EdgeTTS, Instagram)
- [ ] Enough disk space (500+ MB free)
- [ ] No antivirus blocking FFmpeg

If all checked and still failing, create a GitHub issue with:
1. Full error message
2. Output of `pip list`
3. Output of `python --version`
4. Output of `ffmpeg -version`

---

**Related Documentation**:
- [README.md](README.md) - Quick start guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [API_REFERENCE.md](API_REFERENCE.md) - API documentation
