# 🚀 Quick Start Guide - AutoReelBot

**Get your first automated Instagram Reel posted in under 10 minutes!**

This is a beginner-friendly guide that walks you through the complete setup process.

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] **Windows, macOS, or Linux** computer
- [ ] **Internet connection** (required for AI services)
- [ ] **Instagram account** (for uploading)
- [ ] **30 minutes** of free time

---

## Step 1: Install Python

### Windows

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.10** or newer
3. Run installer
4. ✅ **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"
6. Verify installation:
   ```cmd
   python --version
   ```
   Should show: `Python 3.10.x` or higher

### Mac

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Verify
python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv -y

# Verify
python3 --version
```

---

## Step 2: Install FFmpeg

### Windows

**Easy Method** (using Chocolatey):
```powershell
# Install Chocolatey first (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg
```

**Manual Method**:
1. Visit [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Download "Windows builds" (full version)
3. Extract to `C:\ffmpeg`
4. Add to PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add new entry: `C:\ffmpeg\bin`
   - Click OK
   - **Restart your terminal**

**Verify**:
```cmd
ffmpeg -version
```

### Mac

```bash
brew install ffmpeg
ffmpeg -version
```

### Linux

```bash
sudo apt install ffmpeg -y
ffmpeg -version
```

---

## Step 3: Clone or Download Project

### Option A: Using Git (Recommended)

```bash
# Install Git first (if not installed)
# Windows: https://git-scm.com/download/win
# Mac: brew install git
# Linux: sudo apt install git

# Clone repository
git clone https://github.com/yourusername/AutoReelBot.git
cd AutoReelBot
```

### Option B: Download ZIP

1. Download project ZIP file
2. Extract to your desired location
3. Open terminal/command prompt in the extracted folder

---

## Step 4: Setup Virtual Environment

### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try activate again
```

### Windows (Command Prompt)

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

**You should now see `(venv)` in your terminal:**
```
(venv) C:\AutoReelBot>
```

---

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

**Wait 2-3 minutes for installation to complete.**

If you see any red errors, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 6: Get Google Gemini API Key

### 6.1: Create API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with Google account
3. Click **"Create API Key"**
4. Click **"Create API Key in new project"**
5. Copy the key (starts with `AIzaSy...`)

### 6.2: Create `.env` File

**Windows**:
```powershell
# Create .env file
New-Item -Path ".env" -ItemType File

# Open with Notepad
notepad .env
```

**Mac/Linux**:
```bash
# Create and edit .env file
nano .env
```

**Paste this and replace with your key**:
```env
GOOGLE_API_KEY=AIzaSyC_YOUR_ACTUAL_KEY_HERE

# Instagram credentials (optional for now)
INSTA_USERNAME=your_instagram_username
INSTA_PASSWORD=your_instagram_password
```

Save and close the file.

---

## Step 7: Add Images

### 7.1: Create Images Folder

```bash
# Windows
mkdir images

# Mac/Linux
mkdir -p images
```

### 7.2: Add Motivational Images

1. Find or download **6-10 motivational images**
   - Google: "warrior motivational images"
   - Free sources: Unsplash, Pexels, Pixabay

2. Save images to `images/` folder

3. Supported formats: `.jpg`, `.png`, `.jpeg`

4. Recommended: High resolution (1080px+)

**Sample images folder**:
```
images/
├── warrior1.jpg
├── mountain.png
├── sunrise.jpg
├── warrior2.jpg
├── meditation.png
└── victory.jpg
```

---

## Step 8: (Optional) Add Background Music

### 8.1: Create Music Folder

```bash
# Windows
mkdir assets\background_music

# Mac/Linux
mkdir -p assets/background_music
```

### 8.2: Add Music Files

1. Find copyright-free music (YouTube Audio Library, Epidemic Sound)
2. Download as **MP3** format
3. Copy to `assets/background_music/`

**Example**:
```
assets/background_music/
├── epic_motivation.mp3
├── warrior_theme.mp3
└── inspiring_music.mp3
```

---

## Step 9: Test Video Creation

Let's create your first video (without uploading to Instagram):

### 9.1: Run Test Script

```bash
python test_video_editing.py
```

**You should see**:
```
🧠 Generating unique viral content...
✅ Generated unique content
🎙️ Generating Hindi voice-over...
✅ Voice generated (3.2s)
🎬 Creating video with advanced effects...
✅ Video created successfully!
============================================================
📹 File: output/viral_reel.mp4
⏱️  Duration: 18.0s
============================================================
```

### 9.2: Check Output

1. Open `output/` folder
2. Play `viral_reel.mp4`
3. Verify:
   - ✅ Video plays correctly
   - ✅ Images are visible
   - ✅ Voice-over is clear
   - ✅ Background music plays (if added)

**Congratulations! Your first video is created! 🎉**

---

## Step 10: Setup Instagram Upload

### Option A: Username/Password (Simplest)

Already done in Step 6 if you added credentials to `.env`.

### Option B: Session ID (More Secure)

**Why use Session ID?**
- More reliable
- Bypasses password blocks
- Recommended for automation

**How to get Session ID:**

1. **Open Instagram in browser** (logged in)
   - Visit [instagram.com](https://www.instagram.com)
   - Make sure you're logged in

2. **Open DevTools**
   - Press `F12` (Chrome/Edge/Firefox)
   - Or right-click → "Inspect"

3. **Go to Cookies**
   - Click "Application" tab (Chrome/Edge)
   - Or "Storage" tab (Firefox)
   - Expand "Cookies" → `https://www.instagram.com`

4. **Find sessionid**
   - Look for cookie named `sessionid`
   - Click on it
   - Copy the **Value** (long string)

5. **Update `.env` file**
   ```env
   INSTA_SESSIONID=paste_your_copied_sessionid_here
   ```

---

## Step 11: Post Your First Automated Reel!

### 11.1: Run Main Script

```bash
python main.py
```

### 11.2: Expected Output

```
🧹 Workspace cleaned.
🧠 Brainstorming viral hook...
✅ Generated unique content
📜 Hook: सफलता केवल उन्हें मिलती है...
🎙️ Generating voice-over...
✅ Voice: 3.2s
🎬 Creating Viral Reel with Advanced Effects...
🎨 Applying cinematic filter...
⚡ Adding Ken Burns effects...
🎬 Adding transitions...
🎵 Mixing audio...
📦 Rendering final video...
✅ Video created!

🚀 Connecting to Instagram...
✅ Logged in as: @your_username
📤 Uploading reel to Instagram...

🎉 SUCCESS! REEL POSTED!
🔗 URL: https://www.instagram.com/reel/ABC123xyz/
```

### 11.3: Verify Upload

1. Open the URL shown in the output
2. Or visit your Instagram profile
3. Your reel should be live! 🚀

---

## 🎉 Success! What Now?

### Schedule Regular Posts

Run `python main.py` whenever you want to post a new reel!

**Automate with Task Scheduler** (Windows):
1. Open Task Scheduler
2. Create Basic Task
3. Set daily trigger (e.g., 9 AM every day)
4. Action: Start program
5. Program: `C:\Path\To\venv\Scripts\python.exe`
6. Arguments: `C:\Path\To\AutoReelBot\main.py`

**Automate with Cron** (Linux/Mac):
```bash
# Open crontab
crontab -e

# Add line (posts daily at 9 AM)
0 9 * * * cd /path/to/AutoReelBot && ./venv/bin/python main.py
```

### Customize Your Videos

Edit settings in `main.py` or use the advanced API:

```python
from video_editor import create_viral_reel_advanced

# Create custom video
video = create_viral_reel_advanced(
    hindi_text="Your custom Hindi text",
    num_images=8,              # More images
    filter_type="warm",        # Specific filter
    use_transitions=True,
    use_background_music=True
)
```

**Available filters**:
- `cinematic` - Dramatic, desaturated
- `warm` - Golden tones, uplifting
- `cool` - Blue tones, focused

### Best Practices

✅ **DO**:
- Post 1-2 reels per day maximum
- Wait 30+ minutes between posts
- Use high-quality images
- Vary your content themes
- Monitor Instagram analytics

❌ **DON'T**:
- Post more than 10 reels per day
- Use same images repeatedly
- Violate Instagram's Terms of Service
- Use copyrighted music without permission

---

## 🔍 Troubleshooting

### Common Issues

**❌ "No images found"**
```bash
# Add images to images/ folder
# Minimum 6 images required
```

**❌ "FFmpeg not found"**
```bash
# Verify FFmpeg installation
ffmpeg -version

# If missing, reinstall FFmpeg (see Step 2)
```

**❌ "API key missing"**
```bash
# Check .env file exists in project root
# Verify GOOGLE_API_KEY is set correctly
```

**❌ "Instagram login failed"**
```bash
# Get fresh sessionid from browser (Step 10)
# Or use username/password
```

**❌ "Module not found"**
```bash
# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

For more issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📚 Next Steps

- **[README.md](README.md)** - Full documentation
- **[API_REFERENCE.md](API_REFERENCE.md)** - API documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - How it works
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Detailed troubleshooting

---

## 💬 Need Help?

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Search [GitHub Issues](https://github.com/yourusername/AutoReelBot/issues)
3. Create new issue with details

---

## 🎊 Congratulations!

You've successfully set up AutoReelBot and posted your first automated Instagram Reel!

**Share your success**:
- ⭐ Star this repository
- 📱 Share your automated reels on Instagram
- 🤝 Contribute improvements

---

<div align="center">

**Happy Automating! 🚀**

Made with ❤️ for Content Creators

[⬆ Back to Top](#-quick-start-guide---autoreelbot)

</div>
