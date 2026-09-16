import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN_BOT")
MY_UID = 8352636820
BOT_NUMBER = int(os.getenv("BOT_NUMBER", "4"))

SPAM_TEXTS = ["Ả𝗼 𝗠ạ𝗻𝗴 𝗫ã 𝗛ộ𝗶 À 𝗘𝗺 𓀢𓀠"] * 50

is_spamming = False


async def delete_cmd(update):
    try:
        if update.message and update.effective_user and update.effective_user.id == MY_UID:
            await update.message.delete()
    except Exception as e:
        print(f"Lỗi xóa: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    await update.message.reply_text(f"BOT {BOT_NUMBER}: Sẵn sàng!")


async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_spamming
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    if is_spamming:
        return
    is_spamming = True
    asyncio.create_task(spam_loop(update.effective_chat.id, context))


async def spam_loop(chat_id, context):
    global is_spamming
    try:
        while is_spamming:
            for text in SPAM_TEXTS:
                if not is_spamming:
                    break
                await context.bot.send_message(chat_id=chat_id, text=text)
                await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Lỗi bot {BOT_NUMBER}: {e}")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_spamming
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    is_spamming = False


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("all", spam))
    app.add_handler(CommandHandler("dall", stop))
    app.run_polling()
