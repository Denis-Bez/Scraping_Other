import sys

from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationHandlerStop

from Fglaza_Check_Avaible import main_4glaza
from Parser_IShop_Avaible import main_IShop
from bot_handlers import settings
sys.path.append('/home/user/Documents/git')
sys.path.append('/home/user/Documents/git/PP005_Scraping_Santehmoll')
from PP005_Scraping_Santehmoll import main_Smoll
from config import ALLOWED_ID
from bot_keyboards import keyboards
from bot_handlers import settings


# --- Type callback  ---
async def typehandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in ALLOWED_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Entry for your id is disallow')
        raise ApplicationHandlerStop


# --- Command Callback  ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # chat_id = update.effective_chat.id
    # await context.bot.send_message(chat_id=chat_id, text='Bot was running! Your id is {}'.format(chat_id))
    # last_update = main_4glaza.Groups_Ads.Get_last_data_update().strftime('%d-%m-%Y %H:%M')
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Last update was {last_update}')

    await update.message.reply_text("Choose action:", reply_markup=keyboards.start_keyboard())


async def sanmoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await keyboards.query_answer(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Start checking Santehmoll')
    message = main_Smoll.checkAvaible()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def fglaza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await keyboards.query_answer(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Start checking 4glaza')
    message = main_4glaza.Check_avaible()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def ishop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await keyboards.query_answer(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Start checking IShop')
    message = main_IShop.Check_avaible()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def etherum(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Error 404
#     req = requests.get('https://yobit.net/api/3/ticher/eth_usdt')
#     print(f'REsponse: {req}')
#     response = req.json()
#     buy_price = response['eth_usdt']['buy']

#     return f'{datetime.now(),strftime("%Y-%m-%d %H:%M")}\nBuy ETH price: {round(buy_price)} USDT'
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Bot is working!')


# --- Ad's checking  ---
async def choose_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await keyboards.query_answer(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='What do you want to do:', reply_markup=keyboards.scraping_company_keyboard())


async def autocheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await keyboards.query_answer(update)
    settings.job_queue()
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Running checking every day! Start now')


async def one(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=ALLOWED_ID[0], text='One was running!')

async def two(context: ContextTypes.DEFAULT_TYPE):   
    await context.bot.send_message(chat_id=ALLOWED_ID[0], text='Two is running!')
