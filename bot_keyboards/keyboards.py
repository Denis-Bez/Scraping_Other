from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup


# --- Start Bot ---
def start_keyboard():
    keyboard = [
        [InlineKeyboardButton("Ad's Scraping", callback_data='Choose company'), InlineKeyboardButton("Price of etherum", callback_data='etherum')]
    ]       
    return InlineKeyboardMarkup(keyboard)

# --- Ad's checking ---
def scraping_company_keyboard():
    keyboard = [
        [InlineKeyboardButton("Santehmoll", callback_data='Santehmoll'), 
        InlineKeyboardButton("4glaza", callback_data='4glaza'),
        InlineKeyboardButton("IShop", callback_data='IShop')],

        [InlineKeyboardButton("Set autocheck", callback_data='autocheck')]
    ]       
    return InlineKeyboardMarkup(keyboard)

# CallbackQueries need to be answered, even if no notification to the user is needed
async def query_answer(update):
    query = update.callback_query
    await query.answer()
