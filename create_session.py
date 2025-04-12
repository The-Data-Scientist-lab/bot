from telethon import TelegramClient
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram API credentials
API_ID = os.getenv('API_ID', '24107383')
API_HASH = os.getenv('API_HASH', '5c246bb589d22155fac7e56b1c94822c')
PHONE_NUMBER = os.getenv('PHONE_NUMBER', '+919758781006')

async def main():
    print("Creating session file for Render deployment...")
    
    # Use the same session name as in the main script
    session_name = 'render_session'
    
    # Initialize the client
    client = TelegramClient(session_name, API_ID, API_HASH)
    
    # Connect to Telegram
    await client.connect()
    
    # Check if we need to log in
    if not await client.is_user_authorized():
        print("Not authorized. Starting login process...")
        # Send code request
        await client.send_code_request(PHONE_NUMBER)
        print("Verification code sent to your Telegram account")
        
        # Ask for the code
        code = input("Please enter the verification code you received: ")
        
        # Sign in with the code
        await client.sign_in(PHONE_NUMBER, code)
        print("Successfully signed in!")
    else:
        print("Already authorized!")
    
    # Get information about the logged-in user
    me = await client.get_me()
    print(f"Logged in as {me.first_name} {me.last_name if me.last_name else ''} (ID: {me.id})")
    
    # Disconnect the client
    await client.disconnect()
    
    # Check if the session file was created
    session_file = f"{session_name}.session"
    if os.path.exists(session_file):
        print(f"Session file '{session_file}' created successfully!")
        print(f"File size: {os.path.getsize(session_file)} bytes")
        print("You can now upload this file to Render along with your other files.")
    else:
        print("Failed to create session file!")

if __name__ == '__main__':
    asyncio.run(main()) 