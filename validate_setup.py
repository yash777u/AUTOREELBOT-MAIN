"""
Quick validation script to check if GitHub Actions setup is correct
Run this before pushing to GitHub
"""
import os

def check_env():
    """Check if .env file exists and has required variables"""
    print("🔍 Checking .env file...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        return False
    
    required = ['INSTA_USERNAME', 'INSTA_PASSWORD', 'GOOGLE_API_KEY', 'INSTA_SESSIONID']
    
    with open('.env', 'r') as f:
        content = f.read()
    
    missing = []
    for key in required:
        if f"{key}=" in content:
            print(f"✅ {key}: {'*' * 20}")
        else:
            missing.append(key)
    
    if missing:
        print(f"\n❌ Missing: {', '.join(missing)}")
        return False
    
    print("\n✅ All environment variables found!")
    return True

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking required files...")
    
    required_files = [
        'main.py',
        'video_editor.py', 
        'login.py',
        'requirements.txt',
        '.github/workflows/auto-post.yml',
        '.gitignore'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    print("\n✅ All required files present!")
    return True

def check_gitignore():
    """Check if .env is in .gitignore"""
    print("\n🔍 Checking .gitignore...")
    
    if not os.path.exists('.gitignore'):
        print("❌ .gitignore not found!")
        return False
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    if '.env' in content and 'session.json' in content:
        print("✅ .env and session.json are gitignored")
        return True
    else:
        print("❌ .env or session.json not in .gitignore!")
        return False

def main():
    print("=" * 50)
    print("GitHub Actions Setup Validator")
    print("=" * 50)
    
    checks = [
        check_env(),
        check_files(),
        check_gitignore()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("✅ ALL CHECKS PASSED!")
        print("\nNext steps:")
        print("1. Read GITHUB_SETUP.md")
        print("2. Push to GitHub: git add . && git commit -m 'Add workflow' && git push")
        print("3. Add GitHub Secrets (see GITHUB_SETUP.md)")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Fix the issues above before pushing to GitHub")
    print("=" * 50)

if __name__ == "__main__":
    main()
