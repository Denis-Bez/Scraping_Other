import logging
import telegram
from Parser_IShop_Avaible.config import CONFIG

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Application

import asyncio
import sys

from Fglaza_Check_Avaible import main_4glaza
from Parser_IShop_Avaible import main_IShop

sys.path.append('/home/user/Documents/git')
sys.path.append('/home/user/Documents/git/PP005_Scraping_Santehmoll')
from PP005_Scraping_Santehmoll import main_Smoll


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Start checking Santehmoll')
    message = main_Smoll.checkAvaible()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Start checking IShop')
    message = main_IShop.Check_avaible()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Start checking 4glaza')
    message = main_4glaza.Check_avaible()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':  
    application = ApplicationBuilder().token(CONFIG['TOKEN_BOT']).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    start_handler = CommandHandler('help', help)
    application.add_handler(start_handler)

    start_handler = CommandHandler('menu', menu)
    application.add_handler(start_handler)
    
    application.run_polling()