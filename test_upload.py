"""
Simple Reel Upload - Saves sessionid locally for reuse
"""
import os
import time
import random
from dotenv import load_dotenv
from instagrapi import Client

load_dotenv()

USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")
OUTPUT_DIR = "output"
SESSIONID_FILE = ".session_id"


def save_sessionid(sessionid):
    """Save sessionid for next use"""
    try:
        with open(SESSIONID_FILE, 'w') as f:
            f.write(sessionid)
        print(f"💾 SessionID saved")
        return True
    except Exception as e:
        print(f"⚠️ Failed to save: {e}")
        return False


def load_sessionid():
    """Load saved sessionid"""
    if os.path.exists(SESSIONID_FILE):
        try:
            with open(SESSIONID_FILE, 'r') as f:
                sid = f.read().strip()
            if sid:
                print(f"✅ Found saved sessionid")
                return sid
        except:
            pass
    return None


def delete_sessionid():
    """Delete invalid sessionid"""
    try:
        if os.path.exists(SESSIONID_FILE):
            os.remove(SESSIONID_FILE)
            print(f"🗑️ Deleted invalid sessionid")
    except:
        pass


def login():
    """Try saved sessionid first, then username/password"""
    cl = Client()
    
    # Try saved sessionid
    sid = load_sessionid()
    if sid:
        try:
            cl.login_by_sessionid(sid)
            user = cl.account_info()
            print(f"✅ Logged in as @{user.username}")
            return cl
        except:
            print("❌ SessionID expired, using credentials...")
            delete_sessionid()
    
    # Try username/password
    if not USERNAME or not PASSWORD:
        print("❌ Missing INSTA_USERNAME or INSTA_PASSWORD")
        return None
    
    try:
        cl.login(USERNAME, PASSWORD)
        user = cl.account_info()
        print(f"✅ Logged in as @{user.username}")
        
        # Save sessionid for next time
        if hasattr(cl, 'sessionid') and cl.sessionid:
            save_sessionid(cl.sessionid)
        
        return cl
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return None


def upload():
    """Upload reel"""
    reel_path = os.path.join(OUTPUT_DIR, "viral_reel.mp4")
    if not os.path.exists(reel_path):
        print(f"❌ Reel not found: {reel_path}")
        return False
    
    size = os.path.getsize(reel_path) / 1024 / 1024
    print(f"✅ Reel found ({size:.1f} MB)")
    
    thumbnail = os.path.join(OUTPUT_DIR, "viral_reel.mp4.jpg")
    if not os.path.exists(thumbnail):
        thumbnail = None
    
    caption = "🔥 साम्राज्य ज़ीरो से! #motivation #hindi #viral"
    
    # Login
    print("\n🔐 LOGIN")
    print("=" * 60)
    cl = login()
    if not cl:
        return False
    
    # Wait
    delay = random.randint(5, 10)
    print(f"\n⏳ Waiting {delay}s...")
    for i in range(delay, 0, -1):
        print(f"   {i}s", end="\r")
        time.sleep(1)
    
    # Upload
    print("\n\n📤 UPLOAD")
    print("=" * 60)
    print(f"Video: {os.path.basename(reel_path)}")
    print(f"Caption: {caption[:45]}...")
    
    try:
        # Try with thumbnail
        if thumbnail:
            try:
                media = cl.clip_upload(path=reel_path, caption=caption, thumbnail=thumbnail)
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
        media = cl.clip_upload(path=reel_path, caption=caption)
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


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 INSTAGRAM REEL UPLOAD")
    print("=" * 60 + "\n")
    
    success = upload()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ UPLOAD SUCCESSFUL!")
    else:
        print("❌ UPLOAD FAILED")
    print("=" * 60 + "\n")
    
    exit(0)
