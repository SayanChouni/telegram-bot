import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Public + Private Channels
REQUIRED_CHANNELS = [
    "@zecwebdev",          # Public Channel
    "-1003189432861",      # Private
    "-1002680121828",      # Private
    "-1002883674971",      # Private
    "-1003362639452",      # Private
]


# ===========================
#   BUILD JOIN BUTTON LIST
# ===========================
def build_join_keyboard():
    markup = InlineKeyboardMarkup()

    for ch in REQUIRED_CHANNELS:

        # Build correct Join URL
        if ch.startswith("@"):
            url = f"https://t.me/{ch.replace('@', '')}"       # Public
        else:
            url = f"https://t.me/c/{str(ch)[4:]}"             # Private

        # Updated button text (Emoji + Bold style)
        markup.add(
            InlineKeyboardButton(
                text="📌 JOIN CHANNEL",
                url=url
            )
        )

    # Add Check Button
    markup.add(
        InlineKeyboardButton("✅ CHECK JOINED", callback_data="check")
    )

    return markup


# ===========================
#        /start handler
# ===========================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Please join all required channels below:",
        reply_markup=build_join_keyboard()
    )


# ===========================
#    CHECK USER MEMBERSHIP
# ===========================
def user_joined_all(user_id):
    for ch in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(ch, user_id)

            # Not joined
            if member.status in ["left", "kicked"]:
                return False

        except:
            # Cannot access (bot not admin or private channel issue)
            return False

    return True


# ===========================
#   CALLBACK BUTTON ACTION
# ===========================
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
            "❌ Please join *ALL* channels first:",
            reply_markup=build_join_keyboard(),
            parse_mode="Markdown"
        )


# ===========================
#       START BOT
# ===========================
bot.infinity_polling()
