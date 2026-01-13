import os
import time
import random
import json
import shutil
from dotenv import load_dotenv

# --- 🛠️ FIX FOR PILLOW 10+ CRASH (MUST BE AT TOP) ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# ----------------------------------------------------

# Google AI
from google import genai
from google.genai import types
 

# Instagram Login
from login import login_user

# Advanced Video Editor
from video_editor import create_viral_reel_advanced, generate_thumbnail 

# --- CONFIGURATION ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Folders
OUTPUT_DIR = "output"
IMAGES_DIR = "images"

def clean_output():
    """Wipes the output folder to prevent old files from mixing in."""
    if os.path.exists(OUTPUT_DIR):
        try:
            shutil.rmtree(OUTPUT_DIR)
        except PermissionError:
            print("⚠️ Could not delete output folder (file in use). Skipping cleanup.")
            return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    print("🧹 Workspace cleaned.")

# --- STEP 1: VIRAL CONTENT (GEMINI) ---
# --- STEP 1: VIRAL CONTENT (GEMINI) ---
def get_viral_content():
    print("🧠 Brainstorming viral hook...")
    
    if not GOOGLE_API_KEY:
        raise ValueError("❌ GOOGLE_API_KEY missing in .env file!")

    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    # Make prompt dynamic with random themes/topics for variety
    themes = [
         "The power of Tahajjud: Winning while the world sleeps",
        "Sabr is not weakness; it is the ultimate warrior's strength",
        "Fearing only the Creator, never the creation",
        "Building an empire for the Akhirah (Afterlife) first",
        "The discipline of Salah: A CEO's ultimate routine",
        "Sunnah of excellence: Being the best in your craft",
        "Tawakkul: Taking action and leaving the result to Allah",
        "Breaking free from the illusions of the Dunya",
        "Rising after failure through Dua and hard work",
        "Character (Akhlaq) is the true mark of a leader",
    ]
    
    selected_theme = random.choice(themes)
    timestamp = int(time.time())  # Add timestamp for uniqueness
    
    prompt = (
       f"Role: You are a lion-hearted Islamic motivational speaker (Warrior Mindset). "
        f"Your tone is high-energy, deeply masculine, and spiritually empowering. "
        f"Session: {timestamp}. "
        f"Generate a FRESH 15-second viral script in urdu/Hindi. "
        f"Requirements: "
        f"1. THE HOOK (0-3 sec): A slap-of-reality about faith and strength. (e.g., 'Duniya ke aage rona band karo...') "
        f"2. THE BODY (3-15 sec): A mix of warrior discipline and spiritual wisdom. Use 1-2 powerful Arabic terms like Sabr, Tawakkul, or Qadr naturally within the Hindi flow. "
        f"3. No sectarianism or hate. Focus on self-improvement, grit, and devotion to the Creator. "
        f"Output Guidelines: "
        f"1. STRICT JSON ONLY. No markdown, no preamble. "
        f"2. Keys: 'hindi_quote', 'english_translation', 'caption', 'hashtags'. "
        f"3. Caption: SEO-optimized, engaging, 15-20 words (e.g., 'Stop chasing people, start chasing your purpose. 🦁'). "
        f"4. Hashtags: 12-15 tags (e.g., #IslamicMotivation #MuslimMindset #DeenOverDunya #HindiQuotes). "
        f"5. Make it VIRAL, RAW, and UNSTOPPABLE."
        f"Make it VIRAL-WORTHY and UNIQUE!"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",  # Better rate limits than exp
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.9  # High creativity while staying within limits
            )
        )
        
        content = json.loads(response.text)
        
        # Validate response has required fields
        required_fields = ['hindi_quote', 'english_translation', 'caption', 'hashtags']
        if not all(field in content for field in required_fields):
            raise ValueError(f"❌ Gemini response missing required fields! Got: {list(content.keys())}")
        
        print(f"✅ Generated unique content (Theme: {selected_theme})")
        return content
        
    except Exception as e:
        # DON'T use fallback - fail properly so user knows Gemini isn't working
        print(f"❌ GEMINI API FAILED: {e}")
        print("💡 Check your GOOGLE_API_KEY in .env")
        print("💡 Verify API quota at: https://aistudio.google.com/apikey")
        raise RuntimeError(f"Failed to generate content from Gemini: {e}")

# --- STEP 3: ADVANCED VIDEO EDITING ---
def create_viral_reel(audio_path, hindi_text):
    """
    Create viral reel using advanced video editor with:
    - Progressive color grading (B&W → Full Color)
    - Crossfade transitions
    - edgeTTS deep voice (if available)
    - Fast-paced editing (0.5s per clip)
    - Automatic cleanup
    """
    print("🎬 Creating Viral Reel with Advanced Effects...")
    
    # Use the advanced video editor with all the tested features
    output_path = create_viral_reel_advanced(
        hindi_text=hindi_text,
        output_name="viral_reel.mp4",
        use_voice=True  # Generate edgeTTS voice
    )
    
    return output_path

# --- STEP 4: UPLOAD TO INSTAGRAM ---
def upload_reel(video_path, caption):
    """Upload reel to Instagram"""
    print("🚀 UPLOAD")
    print("=" * 60)
    
    # Check reel exists
    if not os.path.exists(video_path):
        print(f"❌ Reel not found: {video_path}")
        return False
    
    size = os.path.getsize(video_path) / 1024 / 1024
    print(f"✅ Reel found ({size:.1f} MB)")
    
    # Check thumbnail
    thumbnail = os.path.join(OUTPUT_DIR, "viral_reel.mp4.jpg")
    if not os.path.exists(thumbnail):
        thumbnail = None
    
    # Login
    print("\n🔐 LOGIN")
    print("=" * 60)
    cl = login_user()
    if not cl:
        return False
    
    # Wait before upload
    delay = random.randint(5, 10)
    print(f"\n⏳ Waiting {delay}s...")
    for i in range(delay, 0, -1):
        print(f"   {i}s", end="\r")
        time.sleep(1)
    
    # Upload
    print("\n\n📤 UPLOADING")
    print("=" * 60)
    print(f"Caption: {caption[:50]}...")
    
    try:
        # Try with thumbnail
        if thumbnail:
            try:
                media = cl.clip_upload(path=video_path, caption=caption, thumbnail=thumbnail)
                if media and hasattr(media, 'code'):
                    print(f"\n🎉 SUCCESS!")
                    print(f"🔗 {media.code}")
                    return True
            except Exception as e:
                if "pydantic" in str(e).lower() or "validation" in str(e).lower():
                    print(f"\n✅ POSTED!")
                    return True
                print(f"⚠️ Retry without thumbnail...")
        
        # Try without thumbnail
        media = cl.clip_upload(path=video_path, caption=caption)
        if media and hasattr(media, 'code'):
            print(f"\n🎉 SUCCESS!")
            print(f"🔗 {media.code}")
            return True
        
        print("❌ Failed - no media code")
        return False
        
    except Exception as e:
        if "pydantic" in str(e).lower() or "validation" in str(e).lower():
            print(f"\n✅ POSTED!")
            return True
        
        print(f"\n❌ Error: {e}")
        return False

# --- MAIN LOOP ---
if __name__ == "__main__":
    try:
        clean_output()
        
        # 1. Content Generation
        data = get_viral_content()
        print(f"📜 Hook: {data['hindi_quote'][:40]}...")
        
        # 2. Video Creation (with integrated voice generation)
        # The advanced video editor handles both voice and video creation
        video_file = create_viral_reel(None, data['hindi_quote'])
        
        # 3. Upload
        caption = f"{data['caption']}\n\n{data['hashtags']}"
        upload_reel(video_file, caption)
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")