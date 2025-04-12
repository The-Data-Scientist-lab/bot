# Telegram Auto-Reply Bot

This bot automatically replies to new messages with a price list and payment instructions.

## Deploy to Render

### Step 1: Create a Session File Locally

Before deploying to Render, you need to create a session file locally:

1. Run the session creation script:
   ```bash
   python create_session.py
   ```

2. Enter the verification code when prompted
3. This will create a file named `render_session.session`
4. Keep this file secure as it contains your login credentials

### Step 2: Deploy to Render

1. Create a free account at [Render.com](https://render.com)

2. Click "New +" and select "Web Service"

3. Connect your GitHub repository or use the "Public Git repository" option

4. Configure your service:
   - Name: `telegram-auto-reply-bot`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python telegram_auto_reply.py`

5. Add these environment variables:
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API Hash
   - `PHONE_NUMBER`: Your phone number with country code

6. **Important**: Upload the session file
   - After creating the service, go to the "Files" tab
   - Upload the `render_session.session` file you created locally
   - This file must be in the root directory of your service

7. Click "Create Web Service"

## Files Required
- telegram_auto_reply.py (main script)
- requirements.txt (dependencies)
- render.yaml (deployment config)
- image.jpg (price list image)
- qrcode.jpg (QR code image)
- render_session.session (created locally)

## Features
- Auto-replies to new messages
- Sends price list and QR code
- Bilingual payment instructions
- Tracks replied users
- Professional formatting with emojis 