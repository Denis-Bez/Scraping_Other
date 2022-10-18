import logging
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Application
from config import CONFIG

import sys
import asyncio

import main_IShop

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message = main_IShop.Check_avaible()
#     message = 'Working!'
#     await update.message.reply_text(message)
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def main():
    bot = telegram.Bot(CONFIG['TOKEN_BOT'])
    message = 'Working!'
    async with bot:
        
        #user_messages = await bot.get_updates()
        # for msg in user_messages:
        #     print(msg['message']['text'])
        
        print(await bot.send_message(text=message, chat_id=CONFIG['CHAT_ID']))

if __name__ == '__main__':
    # application = ApplicationBuilder().token(CONFIG['TOKEN_BOT']).build()
    # start_handler = CommandHandler('start', start)
    # application.add_handler(start_handler)
    # application.run_polling()

    asyncio.run(main())

    