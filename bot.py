import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

REQUIRED_CHANNELS = [
    "@zecwebdev",
    "-1003189432861",
    "-1002680121828",
    "-1002883674971",
    "-1003362639452",
   
]

def build_join_keyboard():
    markup = InlineKeyboardMarkup()
    for ch in REQUIRED_CHANNELS:
        if ch.startswith("@"):
            url = f"https://t.me/{ch.replace('@', '')}"
        else:
            url = f"https://t.me/c/{str(ch)[4:]}"
        markup.add(InlineKeyboardButton(f"Join {ch}", url=url))
    markup.add(InlineKeyboardButton("✅ Check Joined", callback_data="check"))
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Please join all required channels:",
        reply_markup=build_join_keyboard()
    )

def user_joined_all(user_id):
    for ch in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(c):
    user_id = c.from_user.id
    if user_joined_all(user_id):
        bot.send_message(
            c.message.chat.id,
            "🎉 **YOUR REQUEST SUBMITTED SUCCESSFULLY**\nPlease wait for reply.",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            c.message.chat.id,
            "❌ Please join all channels:",
            reply_markup=build_join_keyboard()
        )

bot.infinity_polling()
