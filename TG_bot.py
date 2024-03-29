import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from My_bot_API import API_BOT

def gif_data(gihpy: str, API: str, limit=2):
    response = requests.get("http://api.giphy.com/v1/gifs/search",
                            params = {"q": gihpy,"api_key": API, "limit": limit}).json()
    return (response ["data"], response["meta"]["status"], response["meta"]["msg"])

def url_giphy(giphy_data):
    urls = []
    for i in giphy_data[0]:
        urls.append(i["url"])
    return [urls, giphy_data[1], giphy_data[2]]

logging.basicConfig(
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO
)

async def request_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Giphy_API = "s1FpwS7zuxxEFlU1UNYTaLQmddUh86aL"
    server_giphy_data = url_giphy(gif_data(update.message.text, Giphy_API))
    for i in server_giphy_data[0]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=i)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter the GIF name: ")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=" Hi there, I'm a bot that will help you to receive GIF/n"
                                        "Enter the name of the GIF you want and see what happens: ")

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(API_BOT).build()
    start_handler = CommandHandler('start', start_command)
    app.add_handler(start_handler)
    request = MessageHandler(filters.TEXT & (~filters.COMMAND), request_command)
    app.add_handler(request)

    unknown_handler = MessageHandler(filters.COMMAND, unknown_command)
    app.add_handler(unknown_handler)

    app.run_polling()






