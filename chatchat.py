# rasa run --model models/english.tar.gz --enable-api --cors "*" --port 4020

# rasa train --data data/en --config config.yml --domain domain_en.yml --out models --fixed-model-name model_en

import subprocess
import mysql.connector
import telegram
from telegram import Update
from time import sleep
import requests
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from mysql.connector import OperationalError

def mysql_server_enabling():
    try:
        subprocess.run(['sudo','systemctl','enable','mysql'],check=True)
        print("Mysql server is enabled successfully")
    except subprocess.CalledProcessError as e:
        print(f'Error for enabling mysql server:{e}')

host="localhost"
port=3306
username="root"
password="mysqlsane!4422"
database="michudatabase"


import mysql.connector
from mysql.connector import Error
import time
RASA_API_ENDPOINT_en = 'http://localhost:4020/webhooks/rest/webhook'
INTENT_ENDPOINT_en=    'http://localhost:4020/model/parse'

RASA_API_ENDPOINT_am = 'http://localhost:4030/webhooks/rest/webhook'
INTENT_ENDPOINT_am=    'http://localhost:4030/model/parse'

RASA_API_ENDPOINT_or = 'http://localhost:4040/webhooks/rest/webhook'
INTENT_ENDPOINT_or=    'http://localhost:4040/model/parse'


#TOKEN='5861865205:AAFuE2Ik6XWWLkir39KRw-9fXMciqYL89FQ'
TOKEN='6320973861:AAEO_7-FdnSnKKur2OWWX4BvVJV6-dBJzE0'

def establish_connection(max_retries=5, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            # Establish a connection to the MySQL database
            # connection = mysql.connector.connect(
            #     host="your_host",
            #     user="your_username",
            #     password="your_password",
            #     database="your_database"
            # )
            # print("Connection established successfully!")
            # return connection
            mydb = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database,
            port=port
            )
            print("Connection established successfully!")
            return mydb


        except Error as e:
            print("An error occurred while connecting to the database:", str(e))
            retries += 1
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    print("Maximum number of retries reached. Connection could not be established.")
    return None

# Example usage:
mydb = establish_connection(max_retries=3, retry_delay=10)
if mydb:
    chooseLang=""
    chat_ids=""
    user_data={}
    mycursor=mydb.cursor()
    async def handling_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
        global chooseLang
        username = update.message.from_user.username
        fristName=update.message.from_user.first_name
        chat_ids=update.message.from_user.id
        empty_keyboad=["💬 Comment"]
        query1="SELECT Languages from preferredLanguage WHERE userId=%s"
        valuess=(chat_ids,)
        mycursor.execute(query1, valuess)
        language= mycursor.fetchall()
        print('language', language)
        if language:
            #
            if language[0][0]=="English":
                message_type: str = update.message.chat.type
                text: str = update.message.text
                if text=="📷🧏‍♂️ Rank me":
                    # async def choise_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
                    rank_button=[
                        [
                            InlineKeyboardButton("👍", callback_data="thanks! your feedback keeps me growing"),
                            InlineKeyboardButton("👍👍👍", callback_data="🤷♂️ wow! thank you i realy appreciate your comment"),
                        ],
                        [InlineKeyboardButton("👎", callback_data="Ooh! sorry please put your comment on comment box"),
                            InlineKeyboardButton("👎👎👎",callback_data="🤦♂️ realy I'm so sorry please put your suggestion")],
                    ]

                    reply_rank = InlineKeyboardMarkup(rank_button)

                    await update.message.reply_text("please take a time and rank me", reply_markup=reply_rank)
                elif text in empty_keyboad:
                    await update.message.reply_text("Sorry I am not ready to take comment, I'm under development")
                    # chat_ids=chat_ids
                elif text=="🔠 Language":
                    Lang="none"
                    quert3="UPDATE preferredLanguage SET Languages=%s WHERE userId=%s"
                    values=(Lang,chat_ids)
                    mycursor.execute(quert3,values)
                    mydb.commit()
                    language_button=[
                    [
                        InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
                        InlineKeyboardButton("Ahmaric", callback_data="አማርኛ ቋንቋ ተመርጧል"),
                    ],
                    [InlineKeyboardButton("English", callback_data="English language is activated")],
                    ]

                    reply_language = InlineKeyboardMarkup(language_button)

                    await update.message.reply_text("Okay would you like to change language please choose language you prefer", reply_markup=reply_language)
                else:
                    payload = {
                        'sender': message_type,
                        'message': text
                    }
                    intent_payload={"text":text}
                    user_text=text
                    r = requests.post(RASA_API_ENDPOINT_en, json=payload)
                    await context.bot.send_chat_action(chat_id=chat_ids, action="typing")
                    sleep(1)
                    intent=requests.post(INTENT_ENDPOINT_en, json=intent_payload)

                    response = r.json() #[0]['text']
                    modelIntent=""
                    if intent.status_code==200:
                        modelIntents=intent.json()
                        modelIntent=modelIntents["intent"]["name"]
                    if modelIntent=="greet":
                        text = response[0]['text']+" " +"Mr/Ms"+" "+fristName
                    else:
                        text=response[0]["text"]
                    buttons = response[0].get('buttons', [])
                    if modelIntent=='FAQ':
                        keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload'])] for button in buttons]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        text_values=(username, fristName,user_text, text,chat_ids,modelIntent)
                        userTextQuestion="INSERT INTO chatdata (userName,firstName, userQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                        mycursor.execute(userTextQuestion, text_values)
                        mydb.commit()
                        await update.message.reply_text(text,reply_markup=reply_markup)
                    else:
                        keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload']) for button in buttons]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        text_values=(username, fristName,user_text, text,chat_ids,modelIntent)
                        userTextQuestion="INSERT INTO chatdata (userName,firstName, userQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                        mycursor.execute(userTextQuestion, text_values)
                        mydb.commit()
                        await update.message.reply_text(text,reply_markup=reply_markup)

            elif language[0][0]=="Afaan Oromo":
                message_type: str = update.message.chat.type
                text: str = update.message.text
                print("this is the text in oromic", text)
                if text=="📷🧏‍♂️ Rank me":
                    rank_button=[
                        [
                            InlineKeyboardButton("👍", callback_data="Galatooma! yaadni keessan na jajjabeessa"),
                            InlineKeyboardButton("👍👍👍", callback_data="🤷♂️ wow! ulfaadha isinan dinqisiifadha"),
                        ],
                        [InlineKeyboardButton("👎", callback_data="Ooh! dhiifama yaada keessan naaf katabaa"),
                            InlineKeyboardButton("👎👎👎",callback_data="🤦♂️ dhuugumatti baay'een gadda yaada naaf kenna")],
                    ]

                    reply_rank = InlineKeyboardMarkup(rank_button)

                    await update.message.reply_text("Maalo al-tokko na madaala", reply_markup=reply_rank)
                elif text in empty_keyboad:
                    await update.message.reply_text("Dhifama yaada keessan fudhachuudhaf qoopha'a mitti, galatooma!")
                elif text=="🔠 Language":
                    Lang="duwwa"
                    quert3="UPDATE preferredLanguage SET Languages=%s WHERE userId=%s"
                    user_data[chat_ids]=Lang
                    values=(Lang,chat_ids)
                    mycursor.execute(quert3,values)
                    mydb.commit()
                    language_button=[
                    [
                        InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
                        InlineKeyboardButton("Ahmaric", callback_data="አማርኛ ቋንቋ ተመርጧል"),
                        ],
                    [InlineKeyboardButton("English", callback_data="English language is activated")],
                    ]

                    reply_language = InlineKeyboardMarkup(language_button)

                    await update.message.reply_text("Qooqa jijjiiru barbaaddu ? qooqa barbaaddan filadha", reply_markup=reply_language)
                else:
                    payload = {
                        'sender': message_type,
                        'message': text
                    }
                    intent_payload={"text":text}
                    user_text=text
                    r = requests.post(RASA_API_ENDPOINT_or, json=payload)
                    await context.bot.send_chat_action(chat_id=chat_ids, action="typing")
                    sleep(1)
                    intent=requests.post(INTENT_ENDPOINT_or, json=intent_payload)

                    response = r.json() #[0]['text']
                    modelIntent=""
                    if intent.status_code==200:
                        modelIntents=intent.json()
                        modelIntent=modelIntents["intent"]["name"]
                    if modelIntent=="greet":
                        text = response[0]['text']+" " +"Mr/Ms"+" "+fristName
                    else:
                        text=response[0]["text"]
                    buttons = response[0].get('buttons', [])

                    if modelIntent=='FAQ':
                        keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload'])] for button in buttons]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        print(f'{username}:"this button response",{buttons},"response_text",{text}')
                        text_values=(username, fristName,user_text, text,chat_ids,modelIntent)
                        print("This is query text", text_values)
                        userTextQuestion="INSERT INTO chatdata (userName,firstName, userQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                        mycursor.execute(userTextQuestion, text_values)
                        mydb.commit()
                        await update.message.reply_text(text,reply_markup=reply_markup)

                    else:
                        keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload']) for button in buttons]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        print(f'{username}:"this button response",{buttons},"response_text",{text}')
                        text_values=(username, fristName,user_text, text,chat_ids,modelIntent)
                        print("This is query text", text_values)
                        userTextQuestion="INSERT INTO chatdata (userName,firstName, userQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                        mycursor.execute(userTextQuestion, text_values)
                        mydb.commit()
                        await update.message.reply_text(text,reply_markup=reply_markup)
            elif language[0][0]=="Ahmaric":
                message_type: str = update.message.chat.type
                text: str = update.message.text
                if text=="📷🧏‍♂️ Rank me":
                    # async def choise_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
                    rank_button=[
                        [
                            InlineKeyboardButton("👍", callback_data="እናመሰግናለን!"),
                            InlineKeyboardButton("👍👍👍", callback_data="🤷♂️ ዋው! አመሰግናለሁ"),
                        ],
                        [InlineKeyboardButton("👎", callback_data="ኦሆ! ይቅርታ"),
                            InlineKeyboardButton("👎👎👎",callback_data="🤦♂️ በጣም አዝናለሁ")],
                    ]

                    reply_rank = InlineKeyboardMarkup(rank_button)

                    await update.message.reply_text("እባክዎ ጊዜ ይውሰዱና ደረጃ ይስጡኝ", reply_markup=reply_rank)
                elif text in empty_keyboad:
                    await update.message.reply_text("ይቅርታ አስተያየታችሁን ለመውሰድ ዝግጁ አይደለሁም አመሰግናለሁ")
                elif text=="🔠 Language":
                    Lang="bedo"
                    quert3="UPDATE preferredLanguage SET Languages=%s WHERE userId=%s"
                    user_data[chat_ids]=Lang
                    values=(Lang,chat_ids)
                    mycursor.execute(quert3,values)
                    mydb.commit()
                    language_button=[
                    [
                        InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
                        InlineKeyboardButton("Ahmaric", callback_data="አማርኛ ቋንቋ ተመርጧል"),
                    ],
                    [InlineKeyboardButton("English", callback_data="English language is activated")],
                    ]

                    reply_language = InlineKeyboardMarkup(language_button)

                    await update.message.reply_text("ኦከ ቋንቋ መቀየር ትፈልጋለህ እባክህ የምትፈልገውን ቋንቋ ምረጥ", reply_markup=reply_language)
                else:
                    payload = {
                        'sender': message_type,
                        'message': text
                    }
                    intent_payload={"text":text}
                    user_text=text
                    r = requests.post(RASA_API_ENDPOINT_am, json=payload)
                    await context.bot.send_chat_action(chat_id=chat_ids, action="typing")
                    sleep(1)
                    intent=requests.post(INTENT_ENDPOINT_am, json=intent_payload)

                    response = r.json() #[0]['text']
                    #print("Response",response)
                    modelIntent=""
                    #print(intent.status_code)
                    # if intent.status_code==200:
                    if intent.status_code==200:
                        modelIntents=intent.json()
                        modelIntent=modelIntents["intent"]["name"]
                    #print("this is model intent prediction", modelIntent)
                    if modelIntent=="greet":
                        text = response[0]['text']+" " +"Mr/Ms"+" "+fristName
                    else:
                        text=response[0]["text"]
                    buttons = response[0].get('buttons', [])
                    if modelIntent=='FAQ':
                        keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload'])] for button in buttons]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        text_values=(username, fristName,user_text, text,chat_ids,modelIntent)
                        userTextQuestion="INSERT INTO chatdata (userName,firstName, userQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                        mycursor.execute(userTextQuestion, text_values)
                        mydb.commit()
                        await update.message.reply_text(text,reply_markup=reply_markup)
                    else:
                        keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload']) for button in buttons]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        text_values=(username, fristName,user_text, text,chat_ids,modelIntent)
                        userTextQuestion="INSERT INTO chatdata (userName,firstName, userQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                        mycursor.execute(userTextQuestion, text_values)
                        mydb.commit()
                        await update.message.reply_text(text,reply_markup=reply_markup)
            elif language[0][0]=="none":
                text=update.message.text
                print("this is text", text)
                if text=="📷🧏‍♂️ Rank me":
                    # async def choise_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
                    rank_button=[
                        [
                            InlineKeyboardButton("👍", callback_data="thanks! your feedback keeps me growing"),
                            InlineKeyboardButton("👍👍👍", callback_data="🤷♂️ wow! thank you i realy appreciate your comment"),
                        ],
                        [InlineKeyboardButton("👎", callback_data="Ooh! sorry please put your comment on comment box"),
                            InlineKeyboardButton("👎👎👎",callback_data="🤦♂️ realy I'm so sorry please put your suggestion")],
                    ]

                    reply_rank = InlineKeyboardMarkup(rank_button)
                    await update.message.reply_text("Please take a time and rank me", reply_markup=reply_rank)
                elif text in empty_keyboad:
                    await update.message.reply_text("Sorry I am not ready to take comment, I'm under development")

                else:
                    language_button=[
                            [
                                InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
                                InlineKeyboardButton("Ahmaric", callback_data="አማርኛ ቋንቋ ተመርጧል"),
                            ],
                            [InlineKeyboardButton("English", callback_data="English language is activated")],
                        ]

                    reply_language = InlineKeyboardMarkup(language_button)

                    await update.message.reply_text("you haven't chosen any language please do it to keep up with me", reply_markup=reply_language)

            elif language[0][0]=="bedo":
                text=update.message.text
                if text=="📷🧏‍♂️ Rank me":
                    # async def choise_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
                    rank_button=[
                        [
                            InlineKeyboardButton("👍", callback_data="እናመሰግናለን!"),
                            InlineKeyboardButton("👍👍👍", callback_data="🤷♂️ ዋው! አመሰግናለሁ"),
                        ],
                        [InlineKeyboardButton("👎", callback_data="ኦሆ! ይቅርታ"),
                            InlineKeyboardButton("👎👎👎",callback_data="🤦♂️ በጣም አዝናለሁ")],
                    ]

                    reply_rank = InlineKeyboardMarkup(rank_button)

                    await update.message.reply_text("እባክዎ ጊዜ ይውሰዱና ደረጃ ይስጡኝ", reply_markup=reply_rank)
                elif text in empty_keyboad:
                    await update.message.reply_text("ይቅርታ አስተያየታችሁን ለመውሰድ ዝግጁ አይደለሁም, አመሰግናለሁ !")
                else:
                    language_button=[
                            [
                                InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
                                InlineKeyboardButton("Ahmaric", callback_data="አማርኛ ቋንቋ ተመርጧል"),
                            ],
                            [InlineKeyboardButton("English", callback_data="English language is activated")],
                        ]
                    reply_language = InlineKeyboardMarkup(language_button)

                    await update.message.reply_text("ቋንቋ አልተመረጠም እባክዎን ቋንቋ ይምረጡ", reply_markup=reply_language)

            elif language[0][0]=="duwwa":
                text=update.message.text
                if text=="📷🧏‍♂️ Rank me":
                    # async def choise_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
                    rank_button=[
                        [
                            InlineKeyboardButton("👍", callback_data="Galatooma! yaadni keessan na jajjabeessa"),
                            InlineKeyboardButton("👍👍👍", callback_data="🤷♂️ wow! ulfaadha isinan dinqisiifadha"),
                        ],
                        [InlineKeyboardButton("👎", callback_data="Ooh! dhiifama yaada keessan naaf katabaa"),
                            InlineKeyboardButton("👎👎👎",callback_data="🤦♂️ dhuugumatti baay'een gadda yaada naaf kenna")],
                    ]

                    reply_rank = InlineKeyboardMarkup(rank_button)

                    await update.message.reply_text("Maalo al-tokko na madaala", reply_markup=reply_rank)
                elif text in empty_keyboad:
                    await update.message.reply_text("Dhifama yaada keessan fudhachuudhaf qoopha'a mitti,galatooma!")
                else:
                    language_button=[
                            [
                                InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
                                InlineKeyboardButton("Ahmaric", callback_data="አማርኛ ቋንቋ ተመርጧል"),
                            ],
                            [InlineKeyboardButton("English", callback_data="English language is activated")],
                        ]
                    reply_language = InlineKeyboardMarkup(language_button)

                    await update.message.reply_text("Qooqa hin filanne maalo akka wal hubannuf qooqa filadhaa ", reply_markup=reply_language)

            else:
                message_type: str = update.message.chat.type
                text: str = update.message.text
                reply_keyboard=[['🔠 Language', "💬 Comment"], ["📔 FAQ", "📷🧏♂️ Rank me"]]
                if text=='🔠 Language':
                    language_button=[
                        [
                            InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
                            InlineKeyboardButton("Ahmaric", callback_data="አማርኛ ቋንቋ ተመርጧል"),
                        ],
                        [InlineKeyboardButton("English", callback_data="English language is activated")],
                    ]

                    reply_language = InlineKeyboardMarkup(language_button)

                    await update.message.reply_text("Okay would you like to change language please choose language you preferred", reply_markup=reply_language)

                # elif text=="📷🧏♂️ Rank me":
                #     # async def choise_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
                #     rank_button=[
                #         [
                #             InlineKeyboardButton("👍", callback_data="thanks"),
                #             InlineKeyboardButton("👍👍👍", callback_data="🤷♂️ wow! thank you i realy appreciate your comment"),
                #         ],
                #         [InlineKeyboardButton("👎", callback_data="Ooh! sorry please put your comment on comment box"),
                #             InlineKeyboardButton("👎👎👎",callback_data="🤦♂️ realy I'm so sorry please put your suggestion")],
                #     ]
                #     await update.message.reply_text("Okay would you like to change language please choose language you preferred", reply_markup=reply_language)

                elif text=="📷🧏‍♂️ Rank me":
                    # async def choise_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
                    rank_button=[
                        [
                            InlineKeyboardButton("👍", callback_data="thanks"),
                            InlineKeyboardButton("👍👍👍", callback_data="🤷♂️ wow! thank you i realy appreciate your comment"),
                        ],
                        [InlineKeyboardButton("👎", callback_data="Ooh! sorry please put your comment on comment box"),
                            InlineKeyboardButton("👎👎👎",callback_data="🤦♂️ realy I'm so sorry please put your suggestion")],
                    ]

                    reply_rank = InlineKeyboardMarkup(rank_button)

                    await update.message.reply_text("please take a time and rank me", reply_markup=reply_rank)

                elif text in empty_keyboad:
                    await update.message.reply_text("Sorry I am not ready to take comment, I'm under development")

                else:
                    language_button=[
                            [
                                InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
                                InlineKeyboardButton("Ahmaric", callback_data="አማርኛ ቋንቋ ተመርጧል"),
                            ],
                            [InlineKeyboardButton("English", callback_data="English language is activated")],
                        ]

                    reply_language = InlineKeyboardMarkup(language_button)

                    await update.message.reply_text("You haven't chosen any language please do it to keep up with me", reply_markup=reply_language)

        else:
            text=update.message.text
            print("text",text)
            chat_Id=update.message.from_user.id
            reply_keyboard=[['🔠 Language', "💬 Comment"], ["📔 FAQ", "📷🧏♂️ Rank me"]]
            if text=='🔠 Language':
                query2="INSERT INTO preferredLanguage (userId, Languages) VALUES(%s,%s)"
                mycursor.execute(query2,(chat_Id,chooseLang))
                mydb.commit()
                # user_data[chat_Id]=chooseLang
                # async def choise_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
                language_button=[
                    [
                        InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
                        InlineKeyboardButton("Ahmaric", callback_data="አማርኛ ቋንቋ ተመርጧል"),
                    ],
                    [InlineKeyboardButton("English", callback_data="English language is activated")],
                ]

                reply_language = InlineKeyboardMarkup(language_button)

                await update.message.reply_text("Please choose your preferred language and make chat", reply_markup=reply_language)

            elif text=="📷🧏‍♂️ Rank me":
                # async def choise_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
                rank_button=[
                    [
                        InlineKeyboardButton("👍", callback_data="thanks! your feedback keeps me growing"),
                        InlineKeyboardButton("👍👍👍", callback_data="🤷♂️ wow! thank you i realy appreciate your comment"),
                    ],
                    [InlineKeyboardButton("👎",        callback_data="Ooh! sorry please put your comment on comment box"),
                        InlineKeyboardButton("👎👎👎",callback_data="🤦♂️ realy I'm so sorry please put your suggestion")],
                ]

                reply_rank = InlineKeyboardMarkup(rank_button)

                await update.message.reply_text("please take a time and rank me", reply_markup=reply_rank)

            elif text in empty_keyboad:
                    await update.message.reply_text("Sorry I am not ready to take comment, I'm under development")


            else:
                reply_language=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True )
                await update.message.reply_text('Please use language keyboard button and select language you prefer to chat with me', reply_markup=reply_language)
                #await update.message.reply_text('Please use language keyboard button and select language you prefer to chat with me', reply_markup=reply_lan>



    async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        global chooseLang
        # query = update.callback_query
        # chat_ids=query.from_user.id
        empty_oprions=['none', 'bedo', 'duwwa']
        query = update.callback_query
        payload = query.data
        userInfo=query.message.chat
        chatId=userInfo.id
        user_button=payload
        chat_ids=query.from_user.id

        query1="SELECT Languages from preferredLanguage WHERE userId=%s"
        valuess=(chat_ids,)
        mycursor.execute(query1, valuess)
        language= mycursor.fetchall()

        payload = {
            'sender': query.message.chat_id,
            'message': payload
        }
        callback_options=["🤦♂️ realy I'm so sorry please put your suggestion","እናመሰግናለን!","🤷♂️ ዋው! አመሰግናለሁ","Ooh! sorry please put your comment on comment box","🤷♂️ wow! thank you i realy appreciate your comment",
                          "thanks","thanks! your feedback keeps me growing","🤦♂️ በጣም አዝናለሁ","ኦሆ! ይቅርታ","Galatooma! yaadni keessan na jajjabeessa"
                          ,"🤷♂️ wow! ulfaadha isinan dinqisiifadha","Ooh! dhiifama yaada keessan naaf katabaa","🤦♂️ dhuugumatti baay'een gadda yaada naaf kenna"]

        if language:
            if user_button=='English language is activated':
                Lang="English"
                quert3="UPDATE preferredLanguage SET Languages=%s WHERE userId=%s"
                user_data[chat_ids]=Lang
                values=(Lang,chat_ids)
                mycursor.execute(quert3,values)
                mydb.commit()
                #await context.bot.send_chat_action(chat_id=chatId, action="typing")
                #sleep(2)
                await query.answer()
                await query.edit_message_text(text=f"{query.data}")

            elif user_button=='Afaan oromoo filatame jira':
                Lang="Afaan Oromo"
                quert3="UPDATE preferredLanguage SET Languages=%s WHERE userId=%s"
                values=(Lang,chat_ids)
                mycursor.execute(quert3,values)
                mydb.commit()
                #await context.bot.send_chat_action(chat_id=chatId, action="typing")
                #sleep(2)

                # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
                await query.answer()
                await query.edit_message_text(text=f"{query.data}")
            elif user_button=="አማርኛ ቋንቋ ተመርጧል":
                Lang="Ahmaric"
                quert3="UPDATE preferredLanguage SET Languages=%s WHERE userId=%s"
                values=(Lang,chat_ids)
                mycursor.execute(quert3,values)
                mydb.commit()
                #await context.bot.send_chat_action(chat_id=chatId, action="typing")
                #sleep(2)

                # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

                await query.answer()
                await query.edit_message_text(text=f"{query.data}")
            elif language[0][0] in empty_oprions:
                print("this is enpty option values", query.data)
                await query.answer()
                await query.edit_message_text(text=f"{query.data}")

            elif language[0][0]=='Afaan Oromo':
                query = update.callback_query
                # mysql_server_enabling()
                payload = query.data
                userInfo=query.message.chat
                chatId=userInfo.id
                user_button=payload
                if payload in callback_options:
                    query4="INSERT INTO chatdata (Rank_response, userName, firstName,chatId) VALUES(%s,%s,%s,%s)"
                    values=(payload,userInfo.username, userInfo.first_name,chatId)
                    mycursor.execute(query4,values)
                    mydb.commit()
                    await query.answer()
                    await query.edit_message_text(text=f'{query.data}')
                else:
                    payload = {
                        'sender': query.message.chat_id,
                        'message': payload
                    }
                    #await context.bot.send_chat_action(chat_id=chatId, action="typing")
                    #sleep(2)
                    intent_payload={"text":user_button}
                    r = requests.post(RASA_API_ENDPOINT_or, json=payload)
                    response = r.json()
                    if len(response)<=0:
                        await query.answer()
                        await query.edit_message_text(text=f"{query.data}")
                    else:
                        intent=requests.post(INTENT_ENDPOINT_or, json=intent_payload)
                        modelIntent=""
                        #print(intent.status_code)
                        if intent.status_code==200:
                            modelIntents=intent.json()
                            modelIntent=modelIntents["intent"]["name"]
                        text = response[0]['text']
                        buttons = response[0].get('buttons', [])
                        if len(buttons)<=3:
                            keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload']) for button in buttons]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            userButtonQuestion="INSERT INTO chatdata (userName, firstName, userButtonQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                            button_values=(userInfo.username, userInfo.first_name,user_button, text,chatId,modelIntent)
                            #print("this is button response", button_values)
                            mycursor.execute(userButtonQuestion,button_values)
                            mydb.commit()
                            await query.answer()
                            await query.edit_message_text(text, reply_markup=reply_markup)
                        else:
                            keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload'])] for button in buttons]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            userButtonQuestion="INSERT INTO chatdata (userName, firstName, userButtonQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                            button_values=(userInfo.username, userInfo.first_name,user_button, text,chatId,modelIntent)
                            #print("this is button response", button_values)
                            mycursor.execute(userButtonQuestion,button_values)
                            mydb.commit()
                            await query.answer()
                            await query.edit_message_text(text, reply_markup=reply_markup)
            elif language[0][0]=='English':
                query = update.callback_query
                payload = query.data
                userInfo=query.message.chat
                chatId=userInfo.id
                user_button=payload
                if payload in callback_options:
                    query4="INSERT INTO chatdata (Rank_response, userName, firstName,chatId) VALUES(%s,%s,%s,%s)"
                    values=(payload,userInfo.username, userInfo.first_name,chatId)
                    mycursor.execute(query4,values)
                    mydb.commit()
                    await query.answer()
                    await query.edit_message_text(text=f'{query.data}')
                else:
                    payload = {
                        'sender': query.message.chat_id,
                        'message': payload
                    }
                    #await context.bot.send_chat_action(chat_id=chatId, action="typing")
                    #sleep(2)
                    intent_payload={"text":user_button}
                    r = requests.post(RASA_API_ENDPOINT_en, json=payload)
                    response = r.json()
                    if len(response)<=0:
                        await query.answer()
                        await query.edit_message_text(text=f"{query.data}")
                    else:
                        intent=requests.post(INTENT_ENDPOINT_or, json=intent_payload)
                        modelIntent=""
                        #print(intent.status_code)
                        if intent.status_code==200:
                            modelIntents=intent.json()
                            modelIntent=modelIntents["intent"]["name"]
                        text = response[0]['text']
                        buttons = response[0].get('buttons', [])
                        if len(buttons)<=3:
                            keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload']) for button in buttons]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            userButtonQuestion="INSERT INTO chatdata (userName, firstName, userButtonQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                            button_values=(userInfo.username, userInfo.first_name,user_button, text,chatId,modelIntent)
                            #print("this is button response", button_values)
                            mycursor.execute(userButtonQuestion,button_values)
                            mydb.commit()
                            await query.answer()
                            await query.edit_message_text(text, reply_markup=reply_markup)
                        else:
                            keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload'])] for button in buttons]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            userButtonQuestion="INSERT INTO chatdata (userName, firstName, userButtonQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                            button_values=(userInfo.username, userInfo.first_name,user_button, text,chatId,modelIntent)
                            #print("this is button response", button_values)
                            mycursor.execute(userButtonQuestion,button_values)
                            mydb.commit()
                            await query.answer()
                            await query.edit_message_text(text, reply_markup=reply_markup)
            elif language[0][0]=="Ahmaric":
                query = update.callback_query
                # mysql_server_enabling()
                payload = query.data
                userInfo=query.message.chat
                chatId=userInfo.id
                user_button=payload
                if payload in callback_options:
                    query4="INSERT INTO chatdata (Rank_response, userName, firstName,chatId) VALUES(%s,%s,%s,%s)"
                    values=(payload,userInfo.username, userInfo.first_name,chatId)
                    mycursor.execute(query4,values)
                    mydb.commit()
                    await query.answer()
                    await query.edit_message_text(text=f'{query.data}')
                else:
                    payload = {
                        'sender': query.message.chat_id,
                        'message': payload
                    }
                    #await context.bot.send_chat_action(chat_id=chatId, action="typing")
                    #sleep(2)
                    intent_payload={"text":user_button}
                    r = requests.post(RASA_API_ENDPOINT_am, json=payload)
                    response = r.json()
                    if len(response)<=0:
                        await query.answer()
                        await query.edit_message_text(text=f"{query.data}")

                    else:
                        intent=requests.post(INTENT_ENDPOINT_am, json=intent_payload)
                        modelIntent=""
                        #print(intent.status_code)
                        if intent.status_code==200:
                            modelIntents=intent.json()
                            modelIntent=modelIntents["intent"]["name"]
                        text = response[0]['text']
                        buttons = response[0].get('buttons', [])
                        if len(buttons)<=3:
                            keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload']) for button in buttons]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            userButtonQuestion="INSERT INTO chatdata (userName, firstName, userButtonQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                            button_values=(userInfo.username, userInfo.first_name,user_button, text,chatId,modelIntent)
                            #print("this is button response", button_values)
                            mycursor.execute(userButtonQuestion,button_values)
                            mydb.commit()
                            await query.answer()
                            await query.edit_message_text(text, reply_markup=reply_markup)
                        else:
                            keyboard = [[InlineKeyboardButton(button['title'], callback_data=button['payload'])] for button in buttons]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            userButtonQuestion="INSERT INTO chatdata (userName, firstName, userButtonQuestion,modelAnswers,chatId,modelIntent) VALUES (%s,%s,%s,%s,%s,%s)"
                            button_values=(userInfo.username, userInfo.first_name,user_button, text,chatId,modelIntent)
                            #print("this is button response", button_values)
                            mycursor.execute(userButtonQuestion,button_values)
                            mydb.commit()
                            await query.answer()
                            await query.edit_message_text(text, reply_markup=reply_markup)
                            
            else:
                await query.answer()
                await query.edit_message_text(text=f"{query.data}")

        else:
            print("empty query", query.data)
            await query.answer()
            await query.edit_message_text(text=f"{query.data}")



    #"5861865205:AAFuE2Ik6XWWLkir39KRw-9fXMciqYL89FQ"

    def main() -> None:
        """Run the bot."""
        # Create the Application and pass it your bot's token.
        application = Application.builder().token("5861865205:AAFuE2Ik6XWWLkir39KRw-9fXMciqYL89FQ").build()

        #application.add_handler(CommandHandler("start", start))
        print(chooseLang,"choosen language from main")
        application.add_handler(MessageHandler(filters.TEXT, handling_language))
        application.add_handler(CallbackQueryHandler(button))

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)


    if __name__ == "__main__":
        main()


# mydb.close()

