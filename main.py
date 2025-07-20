import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID", "123456789"))  # Replace 123456789 with your actual chat ID

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running and will send scheduled reminders.")

# Command: /id (optional - to find your chat ID)
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your chat ID is: {update.effective_chat.id}")

# The actual reminder task
async def scheduled_task(bot):
    await bot.send_message(chat_id=CHAT_ID, text="🔔 Reminder: Stay focused and crush your tasks!")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))

    # Setup scheduler
    scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(
        scheduled_task,
        CronTrigger(hour=9, minute=0),  # 9:00 AM daily
        args=[app.bot]
    )
    scheduler.start()

    print("✅ Bot and scheduler started.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
