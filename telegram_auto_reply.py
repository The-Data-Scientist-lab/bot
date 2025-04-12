from telethon import TelegramClient, events
import asyncio
import logging
import os
import json
from telethon.tl.types import User
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram API credentials
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

# Auto-reply message
AUTO_REPLY_MESSAGE = """

⚠️ PLEASE IMAGE BHI OR YE ACCHE SE READ KR LENA -----DHEKO GUYS SIR PRICES AND QR CODE SEND KR DIYA HAI SO PAY KRO OR AND SERVICE LO PLEASE DONT WASTE MY TIME SIDHA BLOCK KR DUNGI OKAY SO PLEASE FALTU KA MESSAGE MT KRNA. ⚠️"""

# Images to send with the auto-reply
PRICE_LIST_IMAGE = "image.jpg"  # First image for price list
QR_CODE_IMAGE = "qrcode.jpg"    # Second image for QR code

# Payment message
PAYMENT_MESSAGE = """⚠️ IMPORTANT NOTICE ⚠️

Dear valued customer 💝

Due to high volume of requests, we prioritize responses to clients who have completed their payment. This helps us maintain quality service for all our clients. 🙈

Please note that replies are only provided after payment confirmation. 💋

Thank you for your understanding and cooperation! 💕

-------------------

⚠️ महत्वपूर्ण सूचना ⚠️

प्रिय ग्राहक 💝

बड़ी संख्या में अनुरोधों के कारण, हम उन ग्राहकों को प्राथमिकता देते हैं जिन्होंने अपना भुगतान पूरा कर लिया है। यह हमें सभी ग्राहकों के लिए गुणवत्तापूर्ण सेवा बनाए रखने में मदद करता है। 🙈

कृपया ध्यान दें कि भुगतान की पुष्टि के बाद ही जवाब दिया जाएगा। 💋

आपके समझने और सहयोग के लिए धन्यवाद! 💕"""

# File to store replied users
REPLIED_USERS_FILE = "replied_users.json"

# Set to store user IDs that have received a reply
replied_users = set()

def load_replied_users():
    global replied_users
    try:
        if os.path.exists(REPLIED_USERS_FILE):
            with open(REPLIED_USERS_FILE, 'r') as f:
                replied_users = set(json.load(f))
            logger.info(f"Loaded {len(replied_users)} replied users")
    except Exception as e:
        logger.error(f"Error loading replied users: {e}")
        replied_users = set()

def save_replied_users():
    try:
        with open(REPLIED_USERS_FILE, 'w') as f:
            json.dump(list(replied_users), f)
    except Exception as e:
        logger.error(f"Error saving replied users: {e}")

# Initialize the client with a custom device name
client = TelegramClient(
    'auto_reply_session', 
    API_ID, 
    API_HASH,
    device_model="Tushar's Auto-Reply",
    system_version="1.0",
    app_version="1.0",
    lang_code="en"
)

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    try:
        # Get sender information
        sender = await event.get_sender()
        chat = await event.get_chat()
        
        # Only handle private chats
        if not isinstance(chat, User):
            return
            
        # Get chat ID and sender name
        chat_id = chat.id  # Keep as integer, don't convert to string yet
        sender_name = f"{getattr(sender, 'first_name', '')} {getattr(sender, 'last_name', '')}".strip()
        
        # Log the message
        logger.info(f"Received message from {sender_name} (ID: {chat_id}): {event.message.text}")
        
        # Check if we've already replied to this user
        if str(chat_id) not in replied_users:  # Convert to string for checking replied_users
            try:
                # Send the price list message
                await event.reply(AUTO_REPLY_MESSAGE)
                logger.info(f"Sent price list to {sender_name}")
                
                # Send the first image (price list)
                if os.path.exists(PRICE_LIST_IMAGE):
                    try:
                        # Get absolute path of image
                        abs_image_path = os.path.abspath(PRICE_LIST_IMAGE)
                        logger.info(f"Sending price list image from: {abs_image_path}")
                        
                        # Send the image using the integer chat_id
                        await client.send_file(
                            chat_id,  # Use integer chat_id here
                            abs_image_path,
                            caption="⚠️ PRICE LIST ⚠️"
                        )
                        logger.info(f"Successfully sent price list image to {sender_name}")
                    except Exception as img_error:
                        logger.error(f"Error sending price list image: {str(img_error)}")
                else:
                    logger.error(f"Price list image file not found at path: {os.path.abspath(PRICE_LIST_IMAGE)}")
                
                # Send the second image (QR code)
                if os.path.exists(QR_CODE_IMAGE):
                    try:
                        # Get absolute path of image
                        abs_qr_path = os.path.abspath(QR_CODE_IMAGE)
                        logger.info(f"Sending QR code image from: {abs_qr_path}")
                        
                        # Send the QR code image
                        await client.send_file(
                            chat_id,
                            abs_qr_path,
                            caption="⚠️ QR CODE AND DETAILS ⚠️"
                        )
                        logger.info(f"Successfully sent QR code image to {sender_name}")
                        
                        # Send the payment message
                        await client.send_message(
                            chat_id,
                            PAYMENT_MESSAGE
                        )
                        logger.info(f"Sent payment message to {sender_name}")
                    except Exception as qr_error:
                        logger.error(f"Error sending QR code image: {str(qr_error)}")
                else:
                    logger.error(f"QR code image file not found at path: {os.path.abspath(QR_CODE_IMAGE)}")
                
                # Mark user as replied (convert chat_id to string for storage)
                replied_users.add(str(chat_id))
                save_replied_users()
                logger.info(f"Marked {sender_name} as replied")
                
            except Exception as e:
                logger.error(f"Error sending reply: {e}")
        else:
            logger.info(f"Already replied to {sender_name} before, skipping")
            
    except Exception as e:
        logger.error(f"Error handling message: {e}")

async def main():
    """Main function to start the client"""
    try:
        logger.info("Starting Telegram auto-reply client...")
        
        # Load replied users list
        load_replied_users()
        
        # Connect to Telegram
        await client.connect()
        
        # Check if we need to log in
        if not await client.is_user_authorized():
            logger.info("Not authorized. Starting login process...")
            await client.start(phone=PHONE_NUMBER)
        else:
            logger.info("Already authorized. Continuing...")
        
        # Get information about the logged-in user
        me = await client.get_me()
        logger.info(f"Logged in as {me.first_name} {me.last_name if me.last_name else ''} (ID: {me.id})")
        
        # Log the absolute path of the image files
        logger.info(f"Price list image path: {os.path.abspath(PRICE_LIST_IMAGE)}")
        if os.path.exists(PRICE_LIST_IMAGE):
            logger.info("Price list image exists and is accessible")
        else:
            logger.error("Price list image not found!")
            
        logger.info(f"QR code image path: {os.path.abspath(QR_CODE_IMAGE)}")
        if os.path.exists(QR_CODE_IMAGE):
            logger.info("QR code image exists and is accessible")
        else:
            logger.error("QR code image not found!")
        
        # Keep the script running
        logger.info("Auto-reply is active. Press Ctrl+C to stop.")
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"Error in main function: {e}")
    finally:
        # Ensure proper cleanup
        await client.disconnect()

if __name__ == '__main__':
    try:
        # Run the main function
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Script stopped by user")
    except Exception as e:
        logger.error(f"Script error: {e}")
    finally:
        # Ensure the client is properly disconnected
        if client.is_connected():
            asyncio.run(client.disconnect()) 