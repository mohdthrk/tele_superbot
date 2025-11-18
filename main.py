
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = os.getenv("8495717635:AAEpGTdwKeCBu0ZzKSQDAETWhhLt9sxxm2I")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Vanakkam! 👋\nTamil songs kekka `/song <song name>` use pannunga 🎵"
    )

async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage:\n/song <song name>")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"Searching Tamil song 🎶: {query}")

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "song.%(ext)s",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch1:{query} Tamil song", download=True)
            file_name = ydl.prepare_filename(result['entries'][0])

        await update.message.reply_audio(audio=open(file_name, "rb"))
        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text("❌ Song download failed.")
        print("ERROR:", e)

BAD_WORDS = [
    "fuck","shit","bitch","punda","pundae","thevidiya","mavan","mf","bc"
]

async def badword_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.lower()
        for w in BAD_WORDS:
            if w in text:
                await update.message.delete()
                return
    except:
        pass

async def link_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.lower()
        if "http://" in text or "https://" in text or "t.me/" in text:
            await update.message.delete()
    except:
        pass

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("song", song))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, badword_filter))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_filter))

app.run_polling()
