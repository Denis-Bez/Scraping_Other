import sys
import datetime

from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationHandlerStop
import requests

from Fglaza_Check_Avaible import main_4glaza
from Parser_IShop_Avaible import main_IShop
from Santehmoll_Avaible import main_Smoll
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
    await update.message.reply_text("Choose action:", reply_markup=keyboards.start_keyboard(context.user_data.get('ads_number', 'Error')))


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

async def santehmoll_new_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text='Start creating new ads!')
    count = main_Smoll.creatingNewAds(context.user_data['ads_number'])
    context.user_data['ads_number'] += 1000
    await query.edit_message_text(text=f"{count} Ads was creating. Current number of ad: {context.user_data.get('ads_number', 'Error')}")


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
    job_smoll = settings.job_queue.run_daily(sanmoll, datetime.time(8, 0, 0, 0), chat_id=update.effective_chat.id)
    job_ishop = settings.job_queue.run_daily(ishop, datetime.time(10, 0, 0, 0), chat_id=update.effective_chat.id)
    job_fglaza = settings.job_queue.run_daily(fglaza, datetime.time(11, 0, 0, 0), chat_id=update.effective_chat.id)
    job_create = settings.job_queue.run_daily(santehmoll_new_ads, datetime.time(12, 0, 0, 0), chat_id=update.effective_chat.id)
    if context.user_data['autocheck'] == 'On':
        job_smoll.schedule_removal()
        job_ishop.schedule_removal()
        job_fglaza.schedule_removal()
        job_create.schedule_removal()
        context.user_data['autocheck'] = 'Off'
        await query.edit_message_text(text='AutoChecking is OFF!')
    else:
        context.user_data['autocheck'] = 'On'
        await query.edit_message_text(text='AutoChecking every day!')



