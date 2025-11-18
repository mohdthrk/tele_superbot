from pyrogram import Client, filters
import re

API_ID = 39223407
API_HASH = "a27928891f9283603dd84e4625fad3c4"
BOT_TOKEN = "8495717635:AAEpGTdwKeCBu0ZzKSQDAETWhhLt9sxxm2I"

app = Client(
    "mybot",
    bot_token=8495717635:AAEpGTdwKeCBu0ZzKSQDAETWhhLt9sxxm2I,
    api_id=39223407,
    api_hash=a27928891f9283603dd84e4625fad3c4
)

# ---------- Delete Links ----------
@app.on_message(filters.group & filters.text)
async def delete_links(_, message):
    if re.search(r"(http|https|t.me|www)", message.text.lower()):
        await message.delete()

# ---------- Delete Bad Words ----------
badwords = [w.strip() for w in open("badwords.txt").readlines()]

@app.on_message(filters.group & filters.text)
async def bad_word_cleaner(_, message):
    text = message.text.lower()
    if any(word in text for word in badwords):
        await message.delete()

# ---------- Remove Fake Users ----------
@app.on_message(filters.new_chat_members)
async def remove_fake(_, message):
    for user in message.new_chat_members:
        if user.username is None:   # fake account
            await message.chat.kick_member(user.id)

# ---------- Welcome Message ----------
@app.on_message(filters.new_chat_members)
async def welcome_message(_, message):
    for user in message.new_chat_members:
        await message.reply_text(f"👋 Welcome {user.mention}!")

# ---------- Music Downloader ----------
@app.on_message(filters.command("song"))
async def song_downloader(_, message):
    try:
        query = message.text.split(" ", 1)[1]
        await message.reply_text(f"🎵 Searching: {query}\n(This feature loading...)")
    except:
        await message.reply_text("Usage:\n/song song name")

app.run()
