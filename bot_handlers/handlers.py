import sys
import datetime

from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationHandlerStop
import requests

from Fglaza_Check_Avaible import main_4glaza
from Parser_IShop_Avaible import main_IShop
# Ubuntu
sys.path.append('/home/user/Documents/git')
sys.path.append('/home/user/Documents/git/PP005_Scraping_Santehmoll')
# Windows
# sys.path.append('C:\\Users\\v4174\\git')
# sys.path.append('C:\\Users\\v4174\\git\\PP005_Scraping_Santehmoll')
from PP005_Scraping_Santehmoll import main_Smoll
from config import ALLOWED_ID
from bot_keyboards import keyboards
from bot_handlers import settings


# --- Type callback  ---
# Checking access to bot
async def typehandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in ALLOWED_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Entry for your id is disallow')
        raise ApplicationHandlerStop


# --- Command Callback  ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choose action:", reply_markup=keyboards.start_keyboard())


async def sanmoll(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text='Start checking Santehmoll')
    message = main_Smoll.checkAvaible()
    await context.bot.send_message(chat_id=context.job.chat_id, text=message)
async def fglaza(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text='Start checking 4glaza')
    message = main_4glaza.Check_avaible()
    await context.bot.send_message(chat_id=context.job.chat_id, text=message)
async def ishop(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text='Start checking IShop')
    message = main_IShop.Check_avaible()
    await context.bot.send_message(chat_id=context.job.chat_id, text=message)

async def sanmoll_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text='Start checking Santehmoll!')
    message = main_Smoll.checkAvaible()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
async def fglaza_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text='Start checking 4glaza!')
    message = main_4glaza.Check_avaible()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
async def ishop_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text='Start checking IShop!')
    message = main_IShop.Check_avaible()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def etherum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    req = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum')
    response = req.json()
    await query.edit_message_text(text=f"📈 Current Etherum price: {response[0]['current_price']}")

# --- Ad's checking  ---
async def choose_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    switch = context.user_data.get('autocheck', 'Off')
    await query.edit_message_text(text='What do you want to do:', reply_markup=keyboards.scraping_company_keyboard(switch))

# Setting the parsers' timer
async def autocheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    settings.job_queue.run_daily(sanmoll, datetime.time(8, 0, 0, 0), chat_id=update.effective_chat.id)
    settings.job_queue.run_daily(ishop, datetime.time(10, 0, 0, 0), chat_id=update.effective_chat.id)
    settings.job_queue.run_daily(fglaza, datetime.time(11, 0, 0, 0), chat_id=update.effective_chat.id)
    context.user_data['autocheck'] = 'On'
    await query.edit_message_text(text='AutoChecking every day!')



