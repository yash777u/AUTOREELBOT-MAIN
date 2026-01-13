"""
Simple Smart Login - Saves sessionid locally for reuse
"""
import os
from dotenv import load_dotenv
from instagrapi import Client

load_dotenv()

USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")
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


def login_user():
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


if __name__ == "__main__":
    login_user()