from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import uuid
import json
from db import init_db, save_user

COUNTRY, CITY = range(2)

with open("countries_cities.json", "r") as f:
    DATA = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[country] for country in DATA.keys()]
    await update.message.reply_text(
        f"Привет, {user.first_name}! Выбери свою страну:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return COUNTRY

async def choose_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = update.message.text
    context.user_data["country"] = country
    cities = DATA.get(country, [])
    keyboard = [[city] for city in cities]
    await update.message.reply_text(
        "Теперь выбери город:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CITY

async def choose_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    country = context.user_data["country"]
    user = update.effective_user
    token = str(uuid.uuid4())

    save_user(user.id, user.full_name, country, city, token)

    map_url = f"https://map.yourdomain.com/map.html?token={token}"
    await update.message.reply_text(
        f"Спасибо, {user.first_name}! 🎉\n"
        f"Ты можешь посмотреть карту здесь:\n{map_url}"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END

def main():
    init_db()
    app = Application.builder().token("
    ").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_country)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_city)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
