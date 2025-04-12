# Telegram Auto-Reply Bot

This bot automatically replies to new messages with a price list and payment instructions.

## Deploy to Render

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

6. Click "Create Web Service"

## Files Required
- telegram_auto_reply.py (main script)
- requirements.txt (dependencies)
- render.yaml (deployment config)
- image.jpg (price list image)
- qrcode.jpg (QR code image)

## Features
- Auto-replies to new messages
- Sends price list and QR code
- Bilingual payment instructions
- Tracks replied users
- Professional formatting with emojis 