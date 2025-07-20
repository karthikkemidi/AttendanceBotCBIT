import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from scraper import get_attendance

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Stores user conversation state
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    user_state[user_id] = {"step": "roll"}
    await update.message.reply_text("🎓 Welcome to CBIT Attendance Bot!\nPlease enter your Roll Number:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    text = update.message.text.strip()

    if user_id not in user_state:
        user_state[user_id] = {"step": "roll"}
        await update.message.reply_text("Please enter your Roll Number:")
        return

    state = user_state[user_id]
    if state["step"] == "roll":
        state["roll"] = text
        state["step"] = "password"
        await update.message.reply_text("🔒 Now enter your Password:")
    elif state["step"] == "password":
        state["password"] = text
        await update.message.reply_text("⏳ Logging in to CBIT ERP and fetching your attendance...")
        attendance = get_attendance(state["roll"], state["password"])
        await update.message.reply_text(f"📊 {attendance}")
        del user_state[user_id]

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("✅ Bot is running...")
    await app.run_polling()

nest_asyncio.apply()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
