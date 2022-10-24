from telegram import Update
from telegram.ext import CommandHandler, TypeHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.ext import ApplicationBuilder

from config import ACCESS_TOKEN
from bot_handlers import handlers
from bot_keyboards import keyboards


# --- Build bot application ---
application = ApplicationBuilder().token(ACCESS_TOKEN).build()

# --- Type handlers ---
application.add_handler(TypeHandler(Update, handlers.typehandler), -1)

# --- Command handlers ---
application.add_handler(CommandHandler('start', handlers.start))
# application.add_handler(CommandHandler('sanmoll', handlers.sanmoll))
# application.add_handler(CommandHandler('fglaza', handlers.fglaza))
# application.add_handler(CommandHandler('ishop', handlers.ishop))

# --- Message handlers  ---
# application.add_handler(MessageHandler(filters.Text(keyboards.start_keyboard[0][0]), handlers.choose_company))

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
    job_queue.run_repeating(handlers.one, interval=60, first=10)
    job_queue.run_repeating(handlers.two, interval=60, first=10)