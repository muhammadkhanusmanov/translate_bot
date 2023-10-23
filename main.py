from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram import Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ChatAdministratorRights

from deep_translator import GoogleTranslator

from db import DB

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


def translate(update:Update, context:CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    text = update.message.text
    db = DB()
    til = db.get_lang(chat_id)
    if til == 'en-uz':
        tr_text = en_uz(text)
    elif til == 'uz-en':
        tr_text = uz_en(text)
    elif til == 'ru-uz':
        tr_text = ru_uz(text)
    else:
        tr_text = uz_ru(text)
    bot.send_message(chat_id, tr_text)
    