import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime

TASKS = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is online!\nUse /add YYYY-MM-DD HH:MM Task")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        parts = context.args
        if len(parts) < 3:
            await update.message.reply_text("❌ Format: /add YYYY-MM-DD HH:MM Task")
            return
        date = parts[0]
        time_str = parts[1]
        task_text = " ".join(parts[2:])
        task_time = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
        TASKS.append((update.effective_chat.id, task_time, task_text))
        await update.message.reply_text(f"✅ Task added for {task_time}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def reminder_loop(app):
    while True:
        now = datetime.now()
        for chat_id, t_time, t_text in TASKS[:]:
            if now >= t_time:
                try:
                    await app.bot.send_message(chat_id=chat_id, text=f"🔔 Reminder: {t_text}")
                    TASKS.remove((chat_id, t_time, t_text))
                except Exception as e:
                    print(e)
        await asyncio.sleep(30)

async def main():
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))

    asyncio.create_task(reminder_loop(app))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
