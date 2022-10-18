import logging
import telegram
from config import CONFIG

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Application

import asyncio
import sys

# Connecting with modeules from patents folders
sys.path.append('/home/user/Documents/git/Scraping_Other')
sys.path.append('/home/user/Documents/git')
sys.path.append('/home/user/Documents/git/PP005_Scraping_Santehmoll')
sys.path.append('/home/user/Documents/git/Scraping_Other/Parser_IShop_Avaible')
sys.path.append('/home/user/Documents/git/Scraping_Other/Fglaza_Check_Avaible')

from Parser_IShop_Avaible import main_IShop
from Fglaza_Check_Avaible import main_4glaza
from PP005_Scraping_Santehmoll import main

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main():
    bot = telegram.Bot(CONFIG['TOKEN_BOT'])
    async with bot:
        # message_IS = main_IShop.Check_avaible()
        # await bot.send_message(text=message_IS, chat_id=CONFIG['CHAT_ID'])

        message_4glaza = main_4glaza.Check_avaible()
        await bot.send_message(text=message_4glaza, chat_id=CONFIG['CHAT_ID'])

        # message_SMoll = main_IShop.checkAvaible()       
        # await bot.send_message(text=message_SMoll, chat_id=CONFIG['CHAT_ID'])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = main_4glaza.Check_avaible()
    await update.message.reply_text(message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':
    # try:
    #     asyncio.run(main())
    # except Exception as Ex:
    #     with open('log.txt', 'a') as file:
    #         file.write(f'Error: {Ex}')
    
    application = ApplicationBuilder().token(CONFIG['TOKEN_BOT']).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()