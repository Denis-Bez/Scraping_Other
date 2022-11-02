from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup

from Fglaza_Check_Avaible import main_4glaza
from Parser_IShop_Avaible import main_IShop
from PP005_Scraping_Santehmoll import main_Smoll

# --- Start Bot ---
def start_keyboard():
    keyboard = [
        [InlineKeyboardButton("Ad's Scraping", callback_data='Choose company'), InlineKeyboardButton("Price of etherum", callback_data='etherum')]
    ]       
    return InlineKeyboardMarkup(keyboard)

# --- Ad's checking ---
def scraping_company_keyboard(switch):
    last_update_4glaza = main_4glaza.Groups_Ads.Get_last_data_update().strftime('%d.%m')
    last_update_IShop = main_IShop.Groups_Ads.Get_last_data_update().strftime('%d.%m')
    last_update_Shmoll = main_Smoll.Groups_Ads.Get_last_data_update().strftime('%d.%m')

    keyboard = [
        [InlineKeyboardButton(f"Santehmoll (Last: {last_update_Shmoll})", callback_data='Santehmoll'), InlineKeyboardButton(f"4glaza (Last: {last_update_4glaza})", callback_data='4glaza')],
        [InlineKeyboardButton(f"IShop (Last: {last_update_IShop})", callback_data='IShop'), InlineKeyboardButton(f"⏰ Set autocheck ({switch})", callback_data='autocheck')]
    ]       
    return InlineKeyboardMarkup(keyboard)