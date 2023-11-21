from flask import Flask, request
import os
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from main import *

TOKEN = os.environ["Token"]

bot = Bot(TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=["POST", "GET"])
def hello():
    if request.method == 'GET':
        return 'hi from Python2022I'
    elif request.method == "POST":
        data = request.get_json(force = True)
        
        dispacher: Dispatcher = Dispatcher(bot, None, workers=0)
        update:Update = Update.de_json(data, bot)

        dispacher.add_handler(CommandHandler('start',start))
        dispacher.add_handler(CommandHandler('uzen',uzen))
        dispacher.add_handler(CommandHandler('enuz',enuz))
        dispacher.add_handler(MessageHandler(Filters.reply,forwarding))
        dispacher.add_handler(CallbackQueryHandler(adminpanel, pattern='admin'))
        dispacher.add_handler(MessageHandler(Filters.text,translate))
        dispacher.add_handler(CallbackQueryHandler(admin_command, pattern='command'))
        dispacher.add_handler(CallbackQueryHandler(checking, pattern='check'))
        #update 
        

        
        dispacher.process_update(update)
        return 'ok'