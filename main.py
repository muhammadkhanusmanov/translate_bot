from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram import Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ChatAdministratorRights

from deep_translator import GoogleTranslator

def en_uz(text):
    tr_text = GoogleTranslator(source='en',target='uz').translate(text)
    return tr_text

def uz_en(text):
    tr_text = GoogleTranslator(source='uz',target='en').translate(text)
    return tr_text

def ru_uz(text):
    tr_text = GoogleTranslator(source='ru',target='uz').translate(text)
    return tr_text

def uz_ru(text):
    tr_text = GoogleTranslator(source='uz',target='ru').translate(text)
    return tr_text


# def en_uz(update:Update, context:CallbackContext):