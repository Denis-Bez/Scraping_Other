from telegram import Update
from telegram.ext import CommandHandler, TypeHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.ext import ApplicationBuilder, Defaults, PicklePersistence

from config import ACCESS_TOKEN, ALLOWED_ID
from bot_handlers import handlers
from bot_keyboards import keyboards

import pytz
import datetime


# --- Build bot application ---
defaults = Defaults(tzinfo=pytz.timezone('Asia/Yekaterinburg'))
persistence = PicklePersistence(filepath="cash_bot")
application = (
    ApplicationBuilder()
    .token(ACCESS_TOKEN)
    .defaults(defaults)
    .persistence(persistence)
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
application.add_handler(CallbackQueryHandler(handlers.sanmoll_key, pattern="^" + 'Santehmoll' + "$"))
application.add_handler(CallbackQueryHandler(handlers.santehmoll_new_ads, pattern="^" + 'Santehmoll_new_ads' + "$"))
application.add_handler(CallbackQueryHandler(handlers.fglaza_key, pattern="^" + '4glaza' + "$"))
application.add_handler(CallbackQueryHandler(handlers.ishop_key, pattern="^" + 'IShop' + "$"))
application.add_handler(CallbackQueryHandler(handlers.autocheck, pattern="^" + 'autocheck' + "$"))


# --- Job Queue  ---
job_queue = application.job_queue