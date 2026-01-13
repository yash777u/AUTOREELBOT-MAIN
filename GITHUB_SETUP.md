# GitHub Actions Setup Guide

## Quick Setup (5 minutes)

### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push
```

### Step 2: Add Secrets
Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 8 secrets:

| Secret Name | Value | Example |
|------------|-------|---------|
| `INSTA_USERNAME` | Your Instagram username | `sanatan.warrior.1` |
| `INSTA_PASSWORD` | Your Instagram password | `Admin@280502` |
| `GOOGLE_API_KEY` | Your Google API key | `AIzaSyCmY...` |
| `INSTA_SESSIONID` | Your Instagram session ID | `68383952591%3A...` |
| `EMAIL_USERNAME` | Gmail for sending errors | `your.email@gmail.com` |
| `EMAIL_PASSWORD` | Gmail app password* | `abcd efgh ijkl mnop` |
| `EMAIL_TO` | Where to receive errors | `your.email@gmail.com` |

**\*Gmail App Password:** Go to https://myaccount.google.com/apppasswords → Generate → Copy the 16-character password

### Step 3: Enable Workflow
1. Go to **Actions** tab in your repo
2. Click "I understand my workflows, go ahead and enable them"
3. Find "Auto Post Reels" workflow
4. Click "Enable workflow"

---

## Schedule
Bot runs automatically **3 times daily**:
- 🌅 **6:00 AM IST** (UTC 0:30)
- ☀️ **2:00 PM IST** (UTC 8:30)
- 🌙 **10:00 PM IST** (UTC 16:30)

---

## Manual Run
To test immediately:
1. Go to **Actions** → **Auto Post Reels**
2. Click **Run workflow** → **Run workflow**

---

## Error Handling
✅ **If bot fails:**
- You'll receive an email with error details
- Logs saved for 7 days in Actions artifacts
- No manual intervention needed

---

## Important Notes
⚠️ **Delete `.env` file** before pushing to GitHub (contains sensitive data)
⚠️ GitHub Actions are free for public repos (2,000 min/month for private)
⚠️ Bot runs on Ubuntu servers (no Windows dependencies)

---

## Troubleshooting

**Email not sending?**
- Verify Gmail app password (not regular password)
- Check if 2FA is enabled on Gmail
- Confirm `EMAIL_USERNAME` and `EMAIL_PASSWORD` secrets

**Bot not running?**
- Check Actions tab for errors
- Verify all 8 secrets are set correctly
- Try manual run first to test

**Instagram login issues?**
- Update `INSTA_SESSIONID` from browser cookies
- Session expires every ~60 days

---

## Quick Commands
```bash
# Push to GitHub
git add .
git commit -m "Update workflow"
git push

# Check workflow status
# Go to: https://github.com/YOUR_USERNAME/AutoReelBot/actions

# View logs
# Actions → Latest run → post-reel → Run bot
```

---

## Security
✅ All credentials stored as GitHub Secrets (encrypted)  
✅ `.env` file should NOT be pushed to GitHub  
✅ Secrets never appear in logs  

**DONE!** Your bot will now post automatically 3x daily 🚀
