# Own Pizza Bot

A Telegram bot for receiving user suggestions and moderating them before publishing to a channel.

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kostya320/own-pizza-bot.git
   cd own-pizza-bot
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Configure environment variables:
   - Rename `.env.dist` to `.env`
   - Fill in the required values

5. Run the bot:
   ```bash
   python3 bot.py
   ```

## ⚙️ Configuration

### Getting BOT_TOKEN:
1. Find @BotFather in Telegram
2. Create a new bot using the `/newbot` command
3. Copy the bot token

### Getting ADMIN_CHAT_ID:
1. Send any message to your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find `chat.id` in the response

### CHANNEL_ID:
- Channel username (e.g., `@your_channel`)
- Or channel ID (e.g., `-1001234567890`)

## 📝 Usage

- Users send messages to the bot
- Messages are forwarded to the admin chat with moderation buttons
- Admin selects "Approve" or "Reject"

## 🛠 Features

- Support for text, photos, videos, documents
- Moderation via buttons
- Action logging
- Error handling