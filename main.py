from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram import (
    Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,
    InlineKeyboardButton,ChatAdministratorRights,ParseMode
    )

from deep_translator import GoogleTranslator

from db import DB

def tekshir(chat_id,bot,channel):
    chan1=bot.getChatMember(channel,str(chat_id))['status']
    if chan1=='left':
        return False
    return True

bot = Bot('5873498271:AAGbWIyvaojE9RZ7HafEVDn2zfU8CVEJ_IY')
def en_uz(text):
    tr_text = GoogleTranslator(source='en',target='uz').translate(text)
    tr_text1 = GoogleTranslator(source='uz',target='en').translate(text)
    return [tr_text,tr_text1]



def translate(update:Update, context:CallbackContext):
    bot=context.bot 
    group_id='1'
    try:
        db = DB()
        chat_id=str(update.message.chat.id)
        if chat_id[0]=='-':
            groups = db.groups()
            group_id = chat_id
            if not(group_id in groups):
                db.addgroup(group_id)   
            chat_id=update.message.from_user.id
        message = update.message
        a = db.check_admins(chat_id)
        msg=False
        addd = False
        remd = False
        addc = False
        removec = False
        if a:
            if group_id[0]=='-':
                text = update.message.text
                tr_text=en_uz(text)
                bot.send_message(group_id, f'*En*\n`{tr_text[1]}`\n\n*Uz*\n`{tr_text[0]}`', parse_mode=ParseMode.MARKDOWN)
                db.save()
                return None
            ruxsat = db.ruxsatlar(chat_id)
            msg = ruxsat['msg']
            addd = ruxsat['addd']
            remd = ruxsat['removed']
            addc = ruxsat['addc']
            removec = ruxsat['removec']
            if msg:
                users = db.allusers()
                if msg:
                    i=0
                    for user in users:
                        try:
                            bot.send_message(f'{user}', message.text)
                            i+=1
                        except:
                            pass
                    bot.send_message(chat_id,f'{i} ta foydalanuvchiga xabar muvafaqiyatli yuborildi')
            elif addd and message.text[:6]=='admin+':
                db.add(message.text[6:],'admin',None)
                try:
                    usr = bot.get_chat(message.text[6:])
                    bot.send_message(chat_id,f'Admin qo\'shildi✅\n\nuser id : {message.text[6:]}\n\nname: {usr.first_name}\n\nusername: {usr.username}')
                except:
                    bot.send_message(chat_id,f'Admin qo\'shildi✅\nUser haqida malumotlar topilmadi')
            elif remd and message.text[:6]=='admin-':
                try:
                    db.delete(message.text[6:])
                    usr = bot.get_chat(message.text[6:])
                    bot.send_message(chat_id,f'Admin o\'chirildi✅\n\nuser id : {message.text[6:]}\n\nname: {usr.first_name}\n\nusername: {usr.username}')
                except:
                    bot.send_message(chat_id,'Admin o\'chirishda xatolik bo\'lishi mumkin tekshirib ko\'ring')
            elif addc and message.text[:8]=='channel+':
                q = db.channel(message.text[8:],'add')
                if q:
                    try:
                        chan1=bot.getChatMember(message.text[8:],chat_id)['status']
                        bot.sendMessage(chat_id,'Chat muvafaqiyatli qo\'shildi✅')
                    except:
                        bot.sendMessage(chat_id,'Kanal qo\'shishda xatolik tekshirib qayta urinib ko\'ring')
                        q=db.channel(message.text[8:],'delete')
            elif (removec and message.text[:8]=='channel-'):
                q=db.channel(message.text[8:],'delete')
                if q:
                    bot.sendMessage(chat_id,'Kanal muvafaqiyatli o\'chirildi')
                else:
                    bot.sendMessage(chat_id,'Kanal o\'chirishda xatolik')
                
            else:
                if group_id!='1':
                    text = update.message.text
                    tr_text=en_uz(text)
                    bot.send_message(group_id, f'*En*\n`{tr_text[1]}`\n\n*Uz*\n`{tr_text[0]}`', parse_mode=ParseMode.MARKDOWN)
                else:
                    text = update.message.text
                    tr_text=en_uz(text)
                    bot.send_message(chat_id, f'*En*\n`{tr_text[1]}`\n\n*Uz*\n`{tr_text[0]}`', parse_mode=ParseMode.MARKDOWN)
        else:
            channels = db.channels()
            if len(channels)!=0:
                for channel in channels:
                    m = tekshir(chat_id,bot,channel)
                    if not(m):
                        bot.send_message(chat_id,'Bot ishlashi uchun qayta /start bosing')
                        db.save()
                        return None
                if group_id!='1':
                    text = update.message.text
                    tr_text=en_uz(text)
                    bot.send_message(group_id, f'*En*\n`{tr_text[1]}`\n\n*Uz*\n`{tr_text[0]}`', parse_mode=ParseMode.MARKDOWN)
                else:
                    text = update.message.text
                    tr_text=en_uz(text)
                    bot.send_message(chat_id, f'*En*\n`{tr_text[1]}`\n\n*Uz*\n`{tr_text[0]}`', parse_mode=ParseMode.MARKDOWN)
            else:
                if group_id!='1':
                    text = update.message.text
                    tr_text=en_uz(text)
                    bot.send_message(group_id, f'*En*\n`{tr_text[1]}`\n\n*Uz*\n`{tr_text[0]}`', parse_mode=ParseMode.MARKDOWN)
                else:
                    text = update.message.text
                    tr_text=en_uz(text)
                    bot.send_message(chat_id, f'*En*\n`{tr_text[1]}`\n\n*Uz*\n`{tr_text[0]}`', parse_mode=ParseMode.MARKDOWN)


    except:
        pass
    db.save()

def start(update:Update,context:CallbackContext):
    bot=context.bot 
    chat_id=str(update.message.chat.id)
    if chat_id[0]=='-':
        return None
    tp = update.message.chat.type
    db = DB()
    a = db.check_admins(chat_id)
    if a:
        btn = InlineKeyboardButton('👤Admin panel', callback_data='admin panel')
        btn1 = InlineKeyboardMarkup([[btn]])
        bot.send_message(chat_id, 'Admin sozlamalari ⚙️', reply_markup=btn1)
    db.starting(chat_id)
    bot.send_message(chat_id, f'User: `{chat_id}`\n\n *Assalomu alaykum tarjimon botga xush kelibsiz*' ,parse_mode=ParseMode.MARKDOWN)
    channels = db.channels()
    admins = db.alladmins()
    if channels!=0 and not(str(chat_id) in admins):
        btn=[]
        for channel in channels:
            btn1 = InlineKeyboardButton('Kanal ➕', callback_data=f'obuna {channel[:3]}',url=f'https://t.me/{channel[1:]}')
            btn.append([btn1])
        btn1 = InlineKeyboardButton('Tekshirish✅', callback_data='check')
        btn.append([btn1])
        btn = InlineKeyboardMarkup(btn)
        bot.sendMessage(chat_id,'Botdan to\'liq foydalanish uchun obunani amalga oshiring',reply_markup=btn)
    db.save()

def uzen(update:Update,context:CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    db = DB()
    db.change(chat_id,'uz-en')
    db.save()
    bot.send_message(chat_id,'Tarjima uchun matn kirgizing')

def enuz(update:Update, context:CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    db = DB()
    db.change(chat_id,'en-uz')
    db.save()
    bot.send_message(chat_id,'Enter text for translation', parse_mode=ParseMode.MARKDOWN)

def adminpanel(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    command = query.data.split(' ')[0]
    db = DB()
    a = db.check_admins(chat_id)
    if a:
        btn1 = InlineKeyboardButton('📨Xabar yuborish', callback_data='command sendmsg')
        btn2 = InlineKeyboardButton('📩Forward yuborish', callback_data='command sendfwd')
        btn3 = InlineKeyboardButton('👤Admin qo\'shish', callback_data='command addadmin')
        btn4 = InlineKeyboardButton('📢Kanal qo\'shish', callback_data='command addchannel')
        btn5 = InlineKeyboardButton('👤Admin o\'chirish', callback_data='command dltadmin')
        btn6 = InlineKeyboardButton('📢Kanal o\'chirish', callback_data='command dltchannel')
        btn7 = InlineKeyboardButton('📄Admin va kanallar', callback_data='command list')
        btn8 = InlineKeyboardButton('📊Statistika', callback_data='command statistik')
        btn = InlineKeyboardMarkup([[btn1,btn2],[btn3,btn4],[btn5,btn6],[btn7],[btn8]])
        bot.delete_message(chat_id=chat_id, message_id=msg)
        bot.sendMessage(chat_id, '*Admin menu*', reply_markup=btn, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.sendMessage(chat_id, 'Bad request')
    db.save()

def admin_command(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    command = query.data.split(' ')[1]
    db = DB()
    a = db.check_admins(chat_id)
    bot.delete_message(chat_id=chat_id, message_id=msg)
    if a:
        db.rmsg(chat_id,False)
        db.rfwd(chat_id,False)
        db.changer(chat_id,'addd')
        db.changer(chat_id,'addc')
        db.changer(chat_id,'removed')
        db.changer(chat_id,'removec')
        if command == 'sendmsg':
            db.rmsg(chat_id,True)
            bot.send_message(chat_id=chat_id, text='Barcha foydalanuvchilarga yuborish uchun text xabar yozing')
        elif command == 'addadmin':
            db.changer(chat_id,'addd',True)
            bot.send_message(chat_id=chat_id, text="Yangi admin qo'shish uchun user_idisini quyidagicha kiriting:\n\nadmin+user_id")
        elif command == 'dltadmin':
           db.changer(chat_id,'removed',True) 
           bot.send_message(chat_id=chat_id, text="Adminni o'cirish uchun user_idisini quyidagicha kiriting:\n\nadmin-user_id") 
        elif command == 'addchannel':
            db.changer(chat_id,'addc',True)
            bot.send_message(chat_id=chat_id, text="Botga majburiy obuna qo'shish uchun birinchi navbatda botni kanalga dmin qiling va quyidagicha kiriting kanal usernameni:\n\nchannel+username")
        elif command == "dltchannel":
            db.changer(chat_id,'removec',True)
            bot.send_message(chat_id=chat_id, text="Majburiy obuna ro'yxatidan kanalni chiqarib tashlash uchun quyidagicha kiriting kanal usernameni:\n\nchannel-username")
        elif command == 'list':
            channels = db.channels()
            if len(channels)!=0:
                text = 'Majburiy obuna uchun kanallar:\n'
                for channel in channels:
                    text+=f'*{channel}*\n'
                bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)
            else:
                bot.sendMessage(chat_id,'Majburiy obuna uchun hech narsa topilmadi',parse_mode=ParseMode.MARKDOWN)
            admins = db.alladmins()
            text = 'Adminlar:\n\n'
            for admin in admins:
                try:
                    usr = bot.get_chat(admin)
                    text += f'User id: `{usr.id}`\nname: `{usr.first_name}`\nusername: `{usr.username}`\n\n'
                except:
                    text += f'User id: `{admin}`'
            bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)
        elif command == 'statistik':
            users = db.allusers()
            groups = db.groups()
            admins = db.alladmins()
            kanals = db.channels()
            text = f'*Bot statistikasi*\n\nAdminlar: {len(admins)}\nUserlar: {len(users)-len(groups)}\nGuruhlar: {len(groups)}\nMajburiy kanallar: {len(kanals)}'
            bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)
        elif command == 'sendfwd':
            bot.sendMessage(chat_id,"*Forward message* yuborish uchun avval yubormoqchi bo'lgan xabaringizni botga yuboring va shu habarni reply qilib *send* xabarini jo'nating",parse_mode=ParseMode.MARKDOWN)
    db.save()

def checking(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    bot.delete_message(chat_id=chat_id, message_id=msg)
    db=DB()
    kanallar = db.channels()
    db.save()
    for kanal in kanallar:
        q = tekshir(chat_id,bot,kanal)
        if not(q):
            bot.send_message(chat_id,'Obunada bo\'lishda xatolik qayta urinib ko\'ring')
            return None
    bot.send_message(chat_id,'Obuna muvafaqqiyatli amalga oshirildi. Botdan foydalanishingiz mumkin.')

def forwarding(update:Update, context:CallbackContext):
    try:
        chat_id = update.message.chat_id
        text = update.message.text
        original_message = update.message.reply_to_message
        db = DB()
        users = db.allusers()
        admins=db.alladmins()
        if not(str(chat_id) in admins and text=='send'):
            db.save()
            return None
        if original_message:
            i=0
            for user in users:
                try:
                    context.bot.forward_message(chat_id=user, from_chat_id=original_message.chat_id, message_id=original_message.message_id)
                    i+=1
                except:
                    pass
            bot.send_message(chat_id,f'{i} ta userga xabar muvafaqiyatli yuborildi')
        else:
            update.message.reply_text("Iltimos, forward qilinayotgan xabarga reply qiling.")
        db.save()
    except:
        pass
            

updater=Updater('5873498271:AAGbWIyvaojE9RZ7HafEVDn2zfU8CVEJ_IY')

updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CommandHandler('uzen',uzen))
updater.dispatcher.add_handler(CommandHandler('enuz',enuz))
updater.dispatcher.add_handler(MessageHandler(Filters.reply,forwarding))
updater.dispatcher.add_handler(CallbackQueryHandler(adminpanel, pattern='admin'))
updater.dispatcher.add_handler(MessageHandler(Filters.text,translate))
updater.dispatcher.add_handler(CallbackQueryHandler(admin_command, pattern='command'))
updater.dispatcher.add_handler(CallbackQueryHandler(checking, pattern='check'))


updater.start_polling()
updater.idle()