from telegram import Update
from telegram.ext import CommandHandler, TypeHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.ext import ApplicationBuilder, Defaults

from config import ACCESS_TOKEN, ALLOWED_ID
from bot_handlers import handlers
from bot_keyboards import keyboards

import pytz
import datetime


# --- Build bot application ---
defaults = Defaults(tzinfo=pytz.timezone('Asia/Yekaterinburg'))
application = (
    ApplicationBuilder()
    .token(ACCESS_TOKEN)
    .defaults(defaults)
    .build()
)

# --- Type handlers ---
application.add_handler(TypeHandler(Update, handlers.typehandler), -1)

# --- Command handlers ---
application.add_handler(CommandHandler('start', handlers.start))

# --- Message handlers  ---


# --- Query handlers  ---
application.add_handler(CallbackQueryHandler(handlers.choose_company, pattern="^" + 'Choose company' + "$"))
application.add_handler(CallbackQueryHandler(handlers.etherum, pattern="^" + 'etherum' + "$"))
application.add_handler(CallbackQueryHandler(handlers.sanmoll, pattern="^" + 'Santehmoll' + "$"))
application.add_handler(CallbackQueryHandler(handlers.fglaza, pattern="^" + '4glaza' + "$"))
application.add_handler(CallbackQueryHandler(handlers.ishop, pattern="^" + 'IShop' + "$"))
application.add_handler(CallbackQueryHandler(handlers.autocheck, pattern="^" + 'autocheck' + "$"))

# --- Job Queue  ---
def job_queue():
    job_queue = application.job_queue
    job_queue.run_daily(handlers.sanmoll, datetime.time(8, 0, 0, 0), user_id=ALLOWED_ID[0])
    job_queue.run_daily(handlers.fglaza, datetime.time(9, 0, 0, 0), user_id=ALLOWED_ID[0])
    job_queue.run_daily(handlers.fglaza, datetime.time(10, 0, 0, 0), user_id=ALLOWED_ID[0])