from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler
import requests
from typing import Final
import re
import bot_db as db

RASA_API_ENDPOINT_en = 'http://63.34.199.220:4020/webhooks/rest/webhook'
INTENT_ENDPOINT_en = 'http://63.34.199.220:4020/model/parse'

RASA_API_ENDPOINT_am = 'http://63.34.199.220:4030/webhooks/rest/webhook'
INTENT_ENDPOINT_am = 'http://63.34.199.220:4030/model/parse'

RASA_API_ENDPOINT_or = 'http://63.34.199.220:4040/webhooks/rest/webhook'
INTENT_ENDPOINT_or = 'http://63.34.199.220:4040/model/parse'

TOKEN: Final = '6320973861:AAECM0Kp2BKT6Ak7s7ERBRzJNCrfDooPvAQ'
BOT_USERNAME: Final = '@MichuCoopBot'


keyboard = [['🔠 English  ||  Afaan Oromo  ||  አማርኛ'],
            ["Michu Channel", "📔 FAQ"],
            ["💬 Comment", "📷🧏 Rank me"]]
reply_keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
keyboard_or = [['🔠 English  ||  Afaan Oromo  ||  አማርኛ'],
               ["Chaanaalii Michu", "📔 FAQ"],
               ["💬 Yaada", "📷🧏 Na Madaala"]]
reply_keyboard_or = ReplyKeyboardMarkup(keyboard_or, resize_keyboard=True)

keyboard_am = [['🔠 English  ||  Afaan Oromo  ||  አማርኛ'],
               ["ሚቹ ቻናል", "📔 FAQ"],
               ["💬 አስተያየት", "📷🧏 ደረጃ ሰጡኝ"]]
reply_keyboard_am = ReplyKeyboardMarkup(keyboard_am, resize_keyboard=True)

# Create an inline keyboard with buttons
language_button = [[
    InlineKeyboardButton("Afaan Oromo", callback_data="Afaan oromoo filatame jira"),
    InlineKeyboardButton("አማርኛ", callback_data="አማርኛ ቋንቋ ተመርጧል")
],
    [InlineKeyboardButton("English", callback_data="English language is activated")]
]
reply_language = InlineKeyboardMarkup(language_button)

rank_button = [[
    InlineKeyboardButton("⭐️⭐️", callback_data="🤦 Really! I'll make every effort to achieve the highest"),
    InlineKeyboardButton("⭐️⭐️⭐️", callback_data="Thanks! your feedback keeps me growing."),
    # InlineKeyboardButton("⭐️⭐️⭐️⭐️", callback_data="Thank you, I'll strive to earn a perfect rating."),
    InlineKeyboardButton("⭐️⭐️⭐️⭐️⭐️", callback_data="🤷 Wow! thank you I really appreciate your rating.")
]
]
reply_rank = InlineKeyboardMarkup(rank_button)

rank_button_or = [[
    InlineKeyboardButton("⭐️⭐️", callback_data="🤦 Waan olaanaa galmaan ga\'uuf carraaqqii hunda nan godha"),
    InlineKeyboardButton("⭐️⭐️⭐️", callback_data="Galatoomi! sadarkaa naaf kennitan akkan guddadhu na taasisa."),
    # InlineKeyboardButton("⭐️⭐️⭐️⭐️", callback_data="Thank you, I'll strive to earn a perfect rating."),
    InlineKeyboardButton("⭐️⭐️⭐️⭐️⭐️", callback_data="🤷 galatoomaa! waan sadarkaa kana naa kennitaniff baayyeen gammadee")
]
]

reply_rank_or = InlineKeyboardMarkup(rank_button_or)

rank_button_am = [
    [
        InlineKeyboardButton("⭐️⭐️", callback_data="🤦 ጥሩ ደረጃ ለማግኘት እጥራለሁ"),
        InlineKeyboardButton("⭐️⭐️⭐️", callback_data="አመሰግናለሁ! አስተያየት ያበረታታኛል!"),
        # InlineKeyboardButton("⭐️⭐️⭐️⭐️", callback_data="Thanks! your feedback keeps me growing."),
        InlineKeyboardButton("⭐️⭐️⭐️⭐️⭐️", callback_data="🤷 ዋዉ! ደረጃ ስለሰጡኝ አመሰግናለሁ")
    ]
]

reply_rank_am = InlineKeyboardMarkup(rank_button_am)

ab_help_am: str = """
*ወደ ሚቹ የእርዳታ ቦት እንኳን ደህና መጣችሁ!*

ከሚቹ ዲጂታል ብድር ጋር የተያያዙ ጠይቆችዎን በሙሉ ለማገዝ ዝግጁ ነኝ ። የሚቺ ዲጂታል ብድር በተመለከተ በሚቀርበው ጥያቄ ላይ ሊተይቡ ይችላሉ እንዲሁም ከመልሱ ጋር አብረው ከሚመጡት አዝራር አርእስቱ የበለጠ ለማወቅ አዝራሩን ይጫኑ።
ልትጠቀምባቸው የምትችላቸው አንዳንድ ትእዛዞች እና ባህሪያት ከታች ናቸው ፥

- */start:* ቦቱ መስራቱን ለማረጋግጥ ወይም መነጋገር ለመጀምር ይጠቅማል ።
- */help፦* ቦቱ እንዴት መጠቀም እንደሚቻል እርዳታ ያግኙ ።
- */about፡* ስለ ምቹ ቦት የበለጠ ይረዱ ።
- */dev፦* ለተጨማሪ ቴክኒካዊ ጉዳይ ወይም እገዛ የቦቱ አብልጻጊዎቸን ያነጋግሩ
- *English  ||  Afaan Oromo  ||  አማርኛ* ፦የሚመርጡትን ቋንቋ ለመቀየር ይህን አዝራር ይጠቀሙ
- *ሚቹ ቻናል*፡ የእኛን ሚቹ ዲጂታል አበዳሪ ማህበረሰቦችን ይቀላቀሉ
- *አስተያየት*፦ የእርስዎን አስተያየት ወይም ጥቆማዎች ያካፍሉን ።
- * 📷🧏 ደረጃ ስጡኝ*፡ በተሞክሮህ መሰረት ቦቱን ደረጃ ስጥ።
- *📔 FAQ*:በብዛት የሚጠየቁ ጥያቄዎች ለመጠየቅ


ማንኛቸውም ጥያቄዎች ካሉዎት ወይም ተጨማሪ እርዳታ ከፈለጉ ለማነጋገር ነፃነት ይሰማዎ። የእርስዎን አስተያየት ዋጋ እንሰጣለን እናም በተቻለ መጠን የተሻለውን አገልግሎት ለእርስዎ ለማቅረብ እንተጋለን!

*ማሳሰቢያ*፡ ከቦት የበለጠ ለማግኘት፣ ጥያቄዎችዎን አጭር እና ትክክለኛ ያድርጉት።

ምቹ የእርዳታ ቦትን ስለመረጡ እናመሰግናለን! 🤖🌟
"""
ab_help_or: str = """
*Baga gara Michu Gargaarsa Bot dhuftan!*

Gaaffii keessan hunda liqii dijitaalaa Michu wajjin walqabatee isin gargaaruuf as jira.Liqii Dijiitaalaa Michu ilaalchisee gaaffii barreessuu dandeessu, dabalataan button debbii jala jiru waa'ee mata duree buttoonichaa caalaatti baruuf buttonincha cuqaasuu dandeessu.
Armaan gaditti ajajoota fi amaloota fayyadamuu dandeessan muraasni:

- */start*: Bot waliin wal qunnamuu jalqabi ykn bot hojechuu isaa ilaali..
- */help*: Akkaataa itti fayyadama bot fi amaloota isaa irratti gargaarsa argadhu.
- */about*: Waa'ee Michu Gargaarsa Bot caalaatti baradhu.
- */dev*: Dhimma teeknikaa ykn gargaarsa dabalataaf kan developer's qunnamaa
- *🔠 English  ||  Afaan Oromo  ||  አማርኛ*: afaan filatte jijjiiruuf button kana fayyadami.
- *💬 Yaada*: Yaada ykn duubdeebii keessan nuuf qoodaa.
- *📷   Rank me*: Muuxannoo kee irratti hundaa'uun bot sadarkaa laatiif.
- *📔 FAQ*: Gaaffiiwwan yeroo baayyee gaafataman argachuu.
- *Michu Channel*: Hawaasa liqii dijitaalaa Michu keenyatti makamaa.

Gaaffii yoo qabaattan ykn gargaarsa dabalataa yoo barbaaddan bilisaan isin qunnamaa. Yaada keessaniif iddoo guddaa kennina, tajaajila hundarra gaarii ta'e isiniif kennuudhaaf carraaqna!

Hubadhu: Bot irraa bu’aa guddaa argachuuf gaaffii keessan gabaabaa fi sirrii ta’e qabadhaa.

Michu Bot filachuu keessaniif galatoomaa! 🤖🌟
"""
ab_help: str = """
*Welcome to Michu Assistance Bot!*

I'm here to assist you with all your queries related to Michu digital lending.You may type in a question regarding Michu Digital Lending, and you may additionally click the inline button to find out more about the button title whenever it appears. 
Below are some commands and features you can use:

- */start:* Begin interacting with the bot or check if the bot is live.
- */help:* Get assistance on how to use the bot and its features.
- */about*: Learn more about Michu Assistance Bot.
- */dev*: Contact the developer's for further technical issue or help
- *🔠 English  ||  Afaan Oromo  ||  አማርኛ*: use this button to change the language you prefer.
- *💬 Comment*: Share your feedback, suggestions, or comments with us.
- *📷🧏 Rank me*: Rank the bot based on your experience.
- *📔 FAQ*: Access frequently asked questions.
- *Michu Channel*: Join our Michu digital lending community.

Feel free to reach out if you have any questions or need further assistance. We value your feedback and strive to provide you with the best service possible!

NB: To get the most out of the bot, keep your inquiries short and precise.

Thank you for choosing Michu Assistance Bot! 🤖🌟 """

ab_about: str = """
*🤖 About Michu Digital Lending Bot*

Welcome to the Michu Digital Lending Bot! 🎉

Our bot is here to provide you with quick and convenient access to information about Michu Digital Lending, a cutting-edge lending platform designed to meet your financial needs.

What can you do with the Michu Digital Lending Bot?

*🔍 Ask Questions*: Have questions about Michu Digital Lending? Simply type your query, and our bot will provide you with relevant information to help you understand our services better.

*📋 Explore Features*: Discover the features and benefits of Michu Digital Lending, including loan options, eligibility criteria, interest rates, and more.

*💬 Get Support*: Need assistance or have specific inquiries? Our bot is here to assist you 24/7, ensuring you receive timely and helpful responses to your queries.

*📢 Stay Informed*: Receive updates, news, and announcements about Michu Digital Lending directly from our bot, keeping you informed about the latest developments and offerings.

We are committed to providing you with a seamless and informative experience through our bot. Feel free to explore and interact with us at any time!

If you have any feedback or suggestions for improving our services, put  it here /dev through our innline command. don't hesitate to let us know. Your input is invaluable to us as we strive to enhance your experience with Michu Digital Lending.

Thank you for choosing Michu Digital Lending Bot! 🌟"""

ab_about_or: str = """
*🤖 Waa'ee Michu Digital Lending Bot*

Baga gara Michu Digital Lending Bot nagaan dhuftan! 🎉

Botiin keenya odeeffannoo waa’ee Michu Digital Lending, waltajjii liqii ammayyaa fedhii maallaqaa keessan guutuuf qophaa’e oddeefanoo saffisaa fi mijataa ta’een argachuuf as jira.

Michu Digital Lending Bot waalin maal gochuu dandeessu?

*🔍 Gaaffii Gaafadhaa*: Waa'ee Michu Digital Lending gaaffii qabduu? Gaaffii keessan salphaatti barreessi, bot keenyas tajaajila keenya caalaatti hubachuuf isin gargaaruuf odeeffannoo barbaachisaa ta'e isiniif kenna.

*📋 Amaloota Qoradhu*: Filannoo liqii, ulaagaalee ulaagaa guutuu, dhala, fi kkf dabalatee amaloota fi faayidaa Michu Digital Lending argadhu.

*💬 Deeggarsa argadhaa*: Gargaarsa barbaadduu moo gaaffii addaa qabduu? Bot keenya 24/7 isin gargaaruuf as jira, gaaffii keessaniif deebii yeroo fi gargaaraa akka argattan mirkaneessa.

*📢 Odeeffannoo Qabaa*: Waa'ee Michu Digital Lending odeeffannoo haaraa, oduu, fi beeksisa kallattiin bot keenya irraa argachuu, waa'ee guddinaa fi dhiyeessii haaraa isin beeksisna.

Muuxannoo gaha fi odeeffannoo qabu karaa bot keenyaa isiniif dhiyeessuuf waadaa seennee jirra. Yeroo barbaaddanitti bilisaan nu qunnamaa!

Tajaajila keenya fooyyessuuf yaada ykn duubdeebii yoo qabaattan as /dev karaa ajaja innline keenyaa kaa'aa. nu beeksisuu irraa duubatti hin jedhinaa. Muuxannoo keessan Michu Digital Lending irratti guddisuuf yeroo carraaqnu galteen keessan gatii guddaa qaba.

Michu Digital Lending Bot filachuu keessaniif galatoomaa!
"""
ab_about_am: str = """
*🤖 ስለ ሚቹ ዲጂታል ብድር ቦት*

ወደ ምቹ ቦት እንኳን በደህና መጡ! 🎉

የኛ ቦት ስለ ሚቹ ዲጂታል ብድር ፈጣን እና ምቹ የሆነ የፋይናንሺያል ፍላጎትን ለማሟላት የተነደፈ የአበዳሪ መድረክ መረጃ ለማግኘት እዚህ መጥቷል።

በሚቹ ዲጂታል ብድር ቦት ምን ማድረግ ይችላሉ?

*🔍 ጥያቄዎችን ጠይቅ*፡ ስለ ሚቹ ዲጂታል ብድር ጥያቄዎች አሉህ? በቀላሉ መጠይቅዎን ይተይቡ፣ እና የእኛ ቦት አገልግሎቶቻችንን በተሻለ ሁኔታ እንዲረዱዎት ጠቃሚ መረጃ ይሰጥዎታል።

*📋 ባህሪያትን አስስ*፡ የብድር አማራጮችን፣ የብቃት መስፈርቶችን፣ የወለድ መጠኖችን እና ሌሎችንም ጨምሮ የሚቹ ዲጂታል ብድርን ባህሪያት እና ጥቅሞችን ያግኙ።

* 💬 ድጋፍ ያግኙ*: እርዳታ ይፈልጋሉ ወይም የተወሰኑ ጥያቄዎች አሉዎት? ለጥያቄዎችዎ ወቅታዊ እና አጋዥ ምላሾችን ማግኘትዎን በማረጋገጥ የእኛ ቦት 24/7 እርስዎን ለመርዳት እዚህ አለ።

*📢 መረጃ ይኑርዎት*፡ ስለ ሚቹ ዲጂታል ብድር በቀጥታ ከቦታችን ይቀበሉ፣ ስለ አዳዲስ ለውጦች እና አቅርቦቶች እርስዎን ያሳውቁን።

በቦታችን በኩል እንከን የለሽ እና መረጃ ሰጭ ተሞክሮ ልንሰጥዎ ቆርጠናል። በማንኛውም ጊዜ እኛን ለማሰስ እና ለመገናኘት ነፃነት ይሰማዎ!

አገልግሎቶቻችንን ለማሻሻል ማንኛውም ግብረመልስ ወይም አስተያየት ካሎት በውስጥ መስመር ትእዛዝ በኩል እዚህ/dev ያስቀምጡት። እኛን ለማሳወቅ አያመንቱ። በሚቹ ዲጂታል ብድር ላይ ያለዎትን ልምድ ለማሳደግ ስንጥር የእርስዎ ግብአት ለእኛ ጠቃሚ ነው።

የምቹ ድጅታል ብድር ቦት ስለመረጡ እናመሰግናለን!
"""
# commands
lang_button = {}
lang_id  = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # global lang_button
    fristName = update.message.from_user.first_name
    user_id = update.message.from_user.id

    text: str = update.message.text

    # print(f'User ({user_id}) {username} {fristName} in {message_type}: "{text}"')
    str_en = "Welcome to the Michu assistance bot. I\'m here to assist you with Michu digital financing. To communicate with me, please select your preferred language from the buttons below."
    str_am = "ወደ ሚቹ የእርዳታ ቦት እንኳን በደህና መጡ። እኔ እዚህ ነኝ በሚቹ ዲጂታል ፋይናንስ ልረዳህ። ከእኔ ጋር ለመገናኘት፣ እባኮትን የሚመርጡትን ቋንቋ ከታች ካሉት አዝራሮች ይምረጡ።"
    str_or = "Gara bot gargaarsa Michu baga nagaan dhuftan. Ani faayinaansii dijitaalaa Michu irratti isin gargaaruuf as jira. Na waliin wal qunnamuuf, mee buttons armaan gadii keessaa afaan barbaadan filadhaa."
    english_resp = f'👋  Hello, {fristName}. Welcome to your Michu assistance bot. I\'m here to help you about Michu digital lending'
    or_resp = f'👋  Akkam jirtu {fristName}. Baga gara bot gargaarsa Michu keessaniitti naagan dhuftan. Waa\'ee liqii dijitaalaa Michu isin gargaaruuf qophidha'
    amh_resp = f'👋  ጤና ይስጥልኝ {fristName}. ወደ ሚቹ አጋዥ ቦት እንኳን በደህና መጡ። ስለ ሚቹ ዲጂታል ብድር እርስዎን ለመርዳት ዝግጁ ነኝ'
    start_resp = f'👋  Hello, {fristName} {str_en} \n\n 👋 Hello {fristName} {str_or} \n\n 👋 ህሎ {fristName} {str_am}'

    # response: str = handle_response(text)
    if user_id in lang_button:
        if lang_button[user_id] == 'English':
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(text= english_resp, reply_markup=reply_keyboard, parse_mode="Markdown")
            # print('BOT:', english_resp)

        elif lang_button[user_id] == 'Afaan Oromo':
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(text=or_resp, reply_markup=reply_keyboard_or, parse_mode="Markdown")
            # print('BOT:', or_resp)

        elif lang_button[user_id] == 'አማርኛ':
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(text=amh_resp, reply_markup=reply_keyboard_am, parse_mode="Markdown")
            # print('BOT:', amh_resp)
        else:
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(text=start_resp, reply_markup=reply_keyboard, parse_mode="Markdown")
            await update.message.reply_text(text="English || Afaan Oromo ||  አማርኛ 👇👇👇", reply_markup=reply_language)
            # print('BOT:', start_resp)
    else:
        await update.message.reply_text(text=start_resp, reply_markup=reply_keyboard, parse_mode="Markdown")
        await update.message.reply_text(text="English || Afaan Oromo ||  አማርኛ 👇👇👇", reply_markup=reply_language)
        # print('BOT:', start_resp)



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # message_type: str = update.message.chat.type
    text: str = update.message.text

    # print(f'User ({user_id}) {username} {fristName} in {message_type}: "{text}"')
    if user_id in lang_button:
        if lang_button[user_id] == 'አማርኛ':
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(ab_help_am, reply_markup=reply_keyboard_am, parse_mode="Markdown")
            # print('BOT:', ab_help_am)
        elif lang_button[user_id] == 'Afaan Oromo':
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(ab_help_or, reply_markup=reply_keyboard_or, parse_mode="Markdown")
            # print('BOT:', ab_help_or)
        else:
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(ab_help, reply_markup=reply_keyboard, parse_mode="Markdown")
            # print('BOT:', ab_help)

    else:
        resp = 'There have been some improvements to the bot; please select a language first to proceed with the latest one.\n\n Fooyya\'iinsi tokko tokko bot kana irratti waan goodhameef; mee dursa afaan filachuun itti fufaa.\n\n በቦቱ ላይ አንዳንድ ማሻሻያዎች ተደርገዋል; ፤ እባክዎ ቋንቋ መርጠው ይቅጥሉ ።'
        await update.message.reply_text(text=resp, reply_markup=reply_language, parse_mode="Markdown")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # global lang_button
    user_id = update.message.from_user.id
    text: str = update.message.text

    # print(f'User ({user_id}) {username} {fristName} in {message_type}: "{text}"')

    if user_id in lang_button:
        if lang_button[user_id] == 'አማርኛ':
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(ab_about_am, reply_markup=reply_keyboard_am, parse_mode="Markdown")
            # print('BOT:', ab_about_am)
        elif lang_button[user_id] == 'Afaan Oromo':
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(ab_about_or, reply_markup=reply_keyboard_or, parse_mode="Markdown")
            # print('BOT:', ab_about_or)
        else:
            db.command(user_id, lang_id[user_id], text)
            await update.message.reply_text(ab_about, reply_markup=reply_keyboard, parse_mode="Markdown")
            # print('BOT:', ab_about)
    else:
        resp = 'There have been some improvements to the bot; please select a language first to proceed with the latest one.\n\n Fooyya\'iinsi tokko tokko bot kana irratti waan goodhameef; mee dursa afaan filachuun itti fufaa.\n\n በቦቱ ላይ አንዳንድ ማሻሻያዎች ተደርገዋል; ፤ እባክዎ ቋንቋ መርጠው ይቅጥሉ ።'
        await update.message.reply_text(text=resp, reply_markup=reply_language, parse_mode="Markdown")
        # print('BOT:', ab_about)


async def dev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Start the conversation
    return await start_dev(update, context)

# Define conversation states
EMAIL, SUGGETION = range(2)
# Start command handler

async def start_dev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # global lang_button
    # Send the first message to start the conversation
    fristName = update.message.from_user.first_name
    chat_ids = update.message.from_user.id
    # print(text)
    response = f"Greetings, {fristName} I appreciate your openness to offer suggestions. We appreciate your feedback and would love to hear from you. \n Please provide your email address."
    response_am = f"ሰላም ፣ {fristName} ፣ አስተያየት ለመስጠት ግልፅ መሆንዎን አደንቃለሁ ። ግብረመልስዎን እናደንቃለን ከእርስዎ መስማት እንፈልጋለን ።እባክዎ የኢሜይል አድራሻዎን ይስጡ"
    response_or = f"Nagaa, {fristName} Yaada nuu kennuu kessaaniif naan dinqisiifadha.  Isin irraas dhaga'uu ni jaallanna. \n Mee email keessan nuuf kenni"
    if chat_ids in lang_button:
        if lang_button[chat_ids] == 'አማርኛ':
            await update.message.reply_text(response_am, reply_markup=reply_keyboard_am)
            # print(response_am)
            return EMAIL
        elif lang_button[chat_ids] == 'Afaan Oromo':
            await update.message.reply_text(response_or, reply_markup=reply_keyboard_or)
            # print(response_or)
            return EMAIL
        else:
            await update.message.reply_text(response, reply_markup=reply_keyboard)
            # print(response)
            return EMAIL
    else:
        resp = 'There have been some improvements to the bot; please select a language first to proceed with the latest one.\n\n Fooyya\'iinsi tokko tokko bot kana irratti waan goodhameef; mee dursa afaan filachuun itti fufaa.\n\n በቦቱ ላይ አንዳንድ ማሻሻያዎች ተደርገዋል; ፤ እባክዎ ቋንቋ መርጠው ይቅጥሉ ።'
        await update.message.reply_text(text=resp, reply_markup=reply_language, parse_mode="Markdown")
        # print(response)
        return ConversationHandler.END


# Email handler
async def email_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract email from user input
    email = update.message.text
    chat_ids = update.message.from_user.id
    context.user_data['email'] = email
    # Regex pattern for email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # print(email)

    # Check if the email matches the pattern
    if re.match(email_pattern, email):
        # Save email to context for later use
        context.user_data['email'] = email
        response = "Kindly provide us with any feedback, suggestions, or comments you may have about this bot.."
        response_am = "ያለዎትን ማንኛውንም ግብረመልስ ፣ ጥቆማዎች ወይም አስተያየቶች በደግነት ያጋሩን.."
        response_or = "yaada, ykn duubdeebii waa'ee bot kanaa qabdan nuuf qooda"
        if chat_ids in lang_button:
            if lang_button[chat_ids] == 'አማርኛ':
                await update.message.reply_text(response_am)
                # print(response_am)
                return SUGGETION
            elif lang_button[chat_ids] == 'Afaan Oromo':
                await update.message.reply_text(response_or)
                # print(response_or)
                return SUGGETION
            else:
                await update.message.reply_text(response)
                # print(response)
                return SUGGETION
        else:
            await update.message.reply_text(response)
            # print(response)
            return SUGGETION

    elif email == '/cancel':
        if chat_ids in lang_button:
            if lang_button[chat_ids] == 'አማርኛ':
                await update.message.reply_text('አስተያየቶ ተሰርዟል ።')
                # print('አስተያየቶ ተሰርዟል ።')
                return ConversationHandler.END
            elif lang_button[chat_ids] == 'Afaan Oromo':
                await update.message.reply_text('yaadinni keessaan haqame.')
                # print('yaadinni keessaan haqame.')
                return ConversationHandler.END
            else:
                await update.message.reply_text('cancelled successfully.')
                # print('cancelled successfully.')
                return ConversationHandler.END
        else:
            await update.message.reply_text('cancelled successfully.')
            # print('cancelled successfully.')
            return ConversationHandler.END
    else:
        # Email format is invalid, prompt the user to enter a valid email
        if chat_ids in lang_button:
            inc_am = "የስገቡት ኢሜይል ልክ አይደለም ። እባክዎ ትክክለኛ የኢሜይል አድራሻ ያስገቡ ። ለማቆም /cancel ይተይቡ "
            inc_or = "email galchitan sirrii miti.  imeelii sirrii ta'e galcha. dhaabuuf /cancel xuqa ykn barreessa"
            inc_en = "The email format is invalid. Please enter a valid email address. type /cancel to stop"
            if lang_button[chat_ids] == 'አማርኛ':
                await update.message.reply_text(inc_am)
                # print(inc_am)
                return EMAIL
            elif lang_button[chat_ids] == 'Afaan Oromo':
                await update.message.reply_text(inc_or)
                # print(inc_or)
                return EMAIL
            else:
                await update.message.reply_text(inc_en)
                # print(inc_en)
                return EMAIL
        else:
            await update.message.reply_text("The email format is invalid. Please enter a valid email address. type /cancel to stop")
            # print(inc_en)
            return EMAIL


async def suggetion_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract suggution from user input
    suggution = update.message.text
    name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    # Save suggution to context for later use
    context.user_data['suggution'] = suggution
    # Retrieve email from context.user_data
    email = context.user_data.get('email', 'Email not provided')
    # print(suggution)
    # print(email)

    # Thank the user for providing information
    response = f"thanks a lot Mr/Ms {name} for your insightful observation! I will contact you via the email address you provided in case you needed any replays or answers."
    response_am = f"ስለ አስተያየቶ በጣም አመስናለው {name}! ማንኛውም መልሶች ቢያስፈልግዎ ፣ ባቀረቡለት የኢሜይል አድራሻ አማካኝነት አገኛችኋለሁ ።"
    response_or = f"Yaada keessaniif baayyee Galatooma Obbo/Aadde {name}!, Yaada keessaniif deebii yoo barbaaddan karaa teessoo email isin kennitan isin qunnama."
    if user_id in lang_button:
        if lang_button[user_id] == 'አማርኛ':
            db.dev(user_id, lang_id[user_id], email, suggution)
            await update.message.reply_text(response_am)
            return ConversationHandler.END
        elif lang_button[user_id] == 'Afaan Oromo':
            db.dev(user_id, lang_id[user_id], email, suggution)
            await update.message.reply_text(response_or)
            return ConversationHandler.END
        else:
            db.dev(user_id, lang_id[user_id], email, suggution)
            await update.message.reply_text(response)
            # print(response)
            return ConversationHandler.END
    else:
        db.dev(user_id, lang_id[user_id], email, suggution)
        await update.message.reply_text(response)
        # print(response)
        return ConversationHandler.END

# Define a function to handle callback queries from inline keyboards

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global lang_button
    query = update.callback_query
    button_data = query.data
    text: str = query.message.text
    # userInfo = query.message.chat.id
    message_type: str = query.message.chat.type

    # Extract the relevant information from the query object
    user_id = query.from_user.id
    userName = query.from_user.username
    firstName = query.from_user.first_name
    # lastName = query.from_user.last_name
    
    # store to data base
    db.userInfo(user_id, userName, firstName)
    
    inline_keyboard = query.message.reply_markup.inline_keyboard

    clicked_button_text = next((button.text for row in inline_keyboard for button in row if button.callback_data == button_data), None)
    # print(clicked_button_text)  # Example: Print the text of each button
    if clicked_button_text in ["Afaan Oromo", "አማርኛ", "English"]:
        lang_button[user_id] = clicked_button_text
    

    clicked_lang_butt = ["Afaan Oromo", "አማርኛ", "English"]
    clicked_rank_butt = ["⭐️⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️", "⭐️⭐️"]
    # keyboard = [['🔠 English  ||  Afaan Oromo  ||  አማርኛ'],
    #         ["Michu Channel", "📔 FAQ"],
    #         ["💬 Comment", "📷🧏 Rank me"]]
    # reply_keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if user_id in lang_button:
        if clicked_button_text in clicked_lang_butt:
            if clicked_button_text == "Afaan Oromo":
                lang_id[user_id] = 2
            elif clicked_button_text == "አማርኛ":
                lang_id[user_id]= 3
            else:
                lang_id[user_id] = 1
            # store to db
            db.userlanguage(lang_id[user_id], clicked_button_text)
            
            if lang_button[user_id] == "አማርኛ": 
                # if data == 'subscribe':
                #     await query.answer("Thanks for subscribing!")
                # elif data == 'learn_more':
                # print(f'User ({user_id}) in {message_type}: "{clicked_button_text}"')
                # print('BOT:', button_data)
                await query.answer(lang_button[user_id])
                await query.edit_message_text(text=f"{button_data}")
                await query.message.reply_text(text=f"እንኳን በደህና መጡ ከአማርኛ ስረት። አሁን ማንኛውንም ጥያቄ በአማርኛ መጠየቅ ይችላሉ", reply_markup= reply_keyboard_am)
            elif lang_button[user_id] == "Afaan Oromo": 
                # print(f'User ({user_id}) in {message_type}: "{clicked_button_text}"')
                # print('BOT:', button_data)
                await query.answer(lang_button[user_id])
                await query.edit_message_text(text=f"{button_data}")
                await query.message.reply_text(text=f"afaan oromo version irraa baga nagaan dhuftan. Amma gaafii kamiyyuu Afaan oromotiin gaafachuu ni dandeessa.", reply_markup= reply_keyboard_or)
            else:
                # print(f'User ({user_id}) in {message_type}: "{clicked_button_text}"')
                # print('BOT:', button_data)
                await query.answer(lang_button[user_id])
                await query.edit_message_text(text=f"{button_data}")
                await query.message.reply_text(text=f"Greetings from the English version. You can now ask any question in English.", reply_markup= reply_keyboard)
        elif clicked_button_text in clicked_rank_butt:
            # store to db
            db.userRank(user_id, lang_id[user_id], clicked_button_text)
            
            # print(f'User ({user_id}) in {message_type}: "{clicked_button_text}"')
            # print('BOT:', button_data)
            await query.answer(f"Thanks mr/ms {firstName} for you rating us!")
            await query.edit_message_text(text=f"{button_data}")
        elif lang_button[user_id] == 'English':
            payload = {
                'sender': query.message.chat_id,
                'message': button_data
            }

            intent_payload = {"text": button_data}
            r = requests.post(RASA_API_ENDPOINT_en, json=payload)
            response = r.json()
            intent = requests.post(INTENT_ENDPOINT_en, json=intent_payload)

            # print(intent.status_code)
            if intent.status_code == 200:
                modelIntent = intent.json()['intent']['name']
                confidence_score = round(intent.json()['intent']['confidence'] if 'confidence' in intent.json()['intent'] else None, 5)
                text = response[0]['text']
                # print(modelIntent)
                buttons = response[0].get('buttons', [])
                # print(f'User ({user_id}) in {message_type}: "{button_data}"')
                await context.bot.send_chat_action(chat_id=user_id, action="typing")
                if modelIntent == 'FAQ':
                    keyboard = [[InlineKeyboardButton( button['title'], callback_data=button['payload'])] for button in buttons]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    # print('BOT:', text)
                    # print(f'confidence: {confidence_score}')
                    
                    db.botAnswer(user_id, lang_id[user_id],  modelIntent, text)
                    db.buttonQuestion(user_id, lang_id[user_id], clicked_button_text, modelIntent, confidence_score, text)
                    await query.answer()
                    await query.edit_message_text(text, reply_markup=reply_markup)
                else:
                    keyboard = [InlineKeyboardButton(
                        button['title'], callback_data=button['payload']) for button in buttons]
                    reply_markup = InlineKeyboardMarkup([keyboard])
                    # response = button_data
                    # print('BOT:', text)
                    # print(f'confidence: {confidence_score}')
                    db.botAnswer(user_id, lang_id[user_id],  modelIntent, text)
                    db.buttonQuestion(user_id, lang_id[user_id], clicked_button_text, modelIntent, confidence_score, text)
                    await query.answer()
                    await query.edit_message_text(text, reply_markup=reply_markup)
            else:
                # Log the error for debugging purposes
                print("Intent API request failed:", intent.status_code)

                # Inform the user that there was an issue processing their request
                error_message = "Sorry, I couldn't process your request at the moment. Please try again later."
                try:
                    await query.answer(error_message)
                except Exception as e:
                    print("Error while sending error message:", str(e))

        elif lang_button[user_id] == 'Afaan Oromo':
            payload = {
                'sender': query.message.chat_id,
                'message': button_data
            }

            intent_payload = {"text": button_data}
            r = requests.post(RASA_API_ENDPOINT_or, json=payload)
            response = r.json()
            intent = requests.post(INTENT_ENDPOINT_or, json=intent_payload)

            # print(intent.status_code)
            if intent.status_code == 200:
                modelIntent = intent.json()['intent']['name']
                confidence_score = round(intent.json()[
                                        'intent']['confidence'] if 'confidence' in intent.json()['intent'] else None, 5)
                text = response[0]['text']
                # print(modelIntent)
                buttons = response[0].get('buttons', [])
                # print(f'User ({user_id}) in {message_type}: "{button_data}"')
                await context.bot.send_chat_action(chat_id=user_id, action="typing")
                if modelIntent == 'FAQ':
                    keyboard = [[InlineKeyboardButton(
                        button['title'], callback_data=button['payload'])] for button in buttons]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    # print('BOT:', text)
                    # print(f'confidence: {confidence_score}')
                    
                    db.botAnswer(user_id, lang_id[user_id],  modelIntent, text)
                    db.buttonQuestion(user_id, lang_id[user_id], clicked_button_text, modelIntent, confidence_score, text)
                    await query.answer()
                    await query.edit_message_text(text, reply_markup=reply_markup)
                else:
                    keyboard = [InlineKeyboardButton(
                        button['title'], callback_data=button['payload']) for button in buttons]
                    reply_markup = InlineKeyboardMarkup([keyboard])
                    # response = button_data
                    # print('BOT:', text)
                    # print(f'confidence: {confidence_score}')
                    
                    db.botAnswer(user_id, lang_id[user_id], modelIntent, text)
                    db.buttonQuestion(user_id, lang_id[user_id], clicked_button_text, modelIntent, confidence_score, text)
                    await query.answer()
                    await query.edit_message_text(text, reply_markup=reply_markup)
            else:
                # Log the error for debugging purposes
                print("Intent API request failed:", intent.status_code)

                # Inform the user that there was an issue processing their request
                error_message = "Sorry, I couldn't process your request at the moment. Please try again later."
                try:
                    await query.answer(error_message)
                except Exception as e:
                    print("Error while sending error message:", str(e))
        elif lang_button[user_id] == 'አማርኛ':
            payload = {
                'sender': query.message.chat_id,
                'message': button_data
            }
            intent_payload = {"text": button_data}
            r = requests.post(RASA_API_ENDPOINT_am, json=payload)
            response = r.json()
            intent = requests.post(INTENT_ENDPOINT_am, json=intent_payload)

            # print(intent.status_code)
            if intent.status_code == 200:
                modelIntent = intent.json()['intent']['name']
                confidence_score = round(intent.json()[
                                        'intent']['confidence'] if 'confidence' in intent.json()['intent'] else None, 5)
                text = response[0]['text']
                # print(modelIntent)
                buttons = response[0].get('buttons', [])
                # print(f'User ({user_id}) in {message_type}: "{button_data}"')
                await context.bot.send_chat_action(chat_id=user_id, action="typing")
                if modelIntent == 'FAQ':
                    keyboard = [[InlineKeyboardButton(
                        button['title'], callback_data=button['payload'])] for button in buttons]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    # print('BOT:', text)
                    # print(f'confidence: {confidence_score}')
                    
                    db.botAnswer(user_id, lang_id[user_id],  modelIntent, text)
                    db.buttonQuestion(user_id, lang_id[user_id], clicked_button_text, modelIntent, confidence_score, text)
                    await query.answer()
                    await query.edit_message_text(text, reply_markup=reply_markup)
                else:
                    keyboard = [InlineKeyboardButton(
                        button['title'], callback_data=button['payload']) for button in buttons]
                    reply_markup = InlineKeyboardMarkup([keyboard])
                    # response = button_data
                    # print('BOT:', text)
                    # print(f'confidence: {confidence_score}')
                    
                    db.botAnswer(user_id, lang_id[user_id],  modelIntent, text)
                    db.buttonQuestion(user_id, lang_id[user_id], clicked_button_text, modelIntent, confidence_score, text)
                    await query.answer()
                    await query.edit_message_text(text, reply_markup=reply_markup)
            else:
                # Log the error for debugging purposes
                print("Intent API request failed:", intent.status_code)

                # Inform the user that there was an issue processing their request
                error_message = "Sorry, I couldn't process your request at the moment. Please try again later."
                try:
                    await query.answer(error_message)
                except Exception as e:
                    print("Error while sending error message:", str(e))
        else:
            await query.edit_message_text(text='There have been some improvements to the bot; please select a language first to proceed with the latest one.', reply_markup=reply_language, parse_mode="Markdown")
    else:
        resp = 'There have been some improvements to the bot; please select a language first to proceed with the latest one.\n\n Fooyya\'iinsi tokko tokko bot kana irratti waan goodhameef; mee dursa afaan filachuun itti fufaa.\n\n በቦቱ ላይ አንዳንድ ማሻሻያዎች ተደርገዋል; ፤ እባክዎ ቋንቋ መርጠው ይቅጥሉ ።'
        await query.message.reply_text(text=resp, reply_markup=reply_language, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fristName = update.message.from_user.first_name
    chat_ids = update.message.from_user.id
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if chat_ids in lang_button:
        select_lang = lang_button[chat_ids]
        if select_lang in ["Afaan Oromo", "አማርኛ", "English"]:
            if select_lang == "English":
                if text == '🔠 English  ||  Afaan Oromo  ||  አማርኛ':
                    await update.message.reply_text(text="Okay would you like to change language please choose language you prefer", reply_markup=reply_language)
                    # print('BOT:', select_lang)
                    # Check if query exists and has data attribute

                    # print(data)
                elif text == '📷🧏 Rank me':
                    # print('BOT:', text)
                    await update.message.reply_text("please take a time and rank me", reply_markup=reply_rank)

                # come back here
                elif text == '💬 Comment':
                    # Start the comment conversation
                    await start_comment(update, context)
                    # put here the comment code here
                    # here if user clilck the comment button from ReplyKeyboardMarkup it take the user comment and responde thanks lastly

                elif text == 'Michu Channel':
                    db.michuChannel(chat_ids, lang_id[chat_ids])
                    await update.message.reply_text('Here is michu channel, join us our community 👇👇👇 \n https://t.me/michudigitallending')

                else:
                    payload = {
                        'sender': message_type,
                        'message': text
                    }
                    intent_payload = {"text": text}

                    # Send message to RASA API endpoint to get response
                    r = requests.post(RASA_API_ENDPOINT_en, json=payload)

                    # Indicate typing action to the user
                    await context.bot.send_chat_action(chat_id=chat_ids, action="typing")
                    # Send message to intent recognition endpoint
                    intent = requests.post(INTENT_ENDPOINT_en, json=intent_payload)
                    if intent.status_code == 200:
                        # Extract response from RASA API
                        response = r.json()

                        # Parse intent and confidence score from the response
                        modelIntent = intent.json()['intent']['name']
                        confidence_score = round(intent.json()['intent']['confidence'] if 'confidence' in intent.json()['intent'] else None, 5)

                        # Handle response based on model intent
                        if modelIntent == "greet":
                            respp = response[0]['text'] + " " + "Mr/Ms" + " " + fristName
                        else:
                            respp = response[0]["text"]

                        # Extract buttons from response
                        buttons = response[0].get('buttons', [])

                        # Check if the model intent is 'FAQ'
                        if modelIntent == 'FAQ':
                            # Create inline keyboard markup for FAQ response
                            keyboard = [[InlineKeyboardButton(
                                button['title'], callback_data=button['payload'])] for button in buttons]
                            reply_markup = InlineKeyboardMarkup(keyboard)

                        else:
                            # Create inline keyboard markup for other responses
                            keyboard = [InlineKeyboardButton(
                                button['title'], callback_data=button['payload']) for button in buttons]
                            reply_markup = InlineKeyboardMarkup([keyboard])

                        # Reply to the user with the message and inline keyboard markup
                        # Print model prediction and confidence
                        # print('BOT:', text)
                        # print('Confidence:', confidence_score)
                        # print(modelIntent)
                        db.botAnswer(chat_ids, lang_id[chat_ids],  modelIntent, respp)
                        db.textQuestion(chat_ids, lang_id[chat_ids], text, modelIntent, confidence_score, respp)
                        await update.message.reply_text(text= respp, reply_markup=reply_markup)
                    else:
                        # Log the error for debugging purposes
                        # print("Intent API request failed:", intent.status_code)

                        # Inform the user that there was an issue processing their request
                        error_message = "Sorry, I couldn't process your request at the moment. Please try again later."
                        await update.message.reply_text(error_message)
            elif select_lang == "Afaan Oromo":
                if text == '🔠 English  ||  Afaan Oromo  ||  አማርኛ':
                    # for row in reply_language.inline_keyboard:
                    #     for button in row:
                    #         print(button.text)
                    # print('BOT:', text)
                    await update.message.reply_text(text="afaan jijjiiruu barbaadduu?, mee afaan Barbaadan filadhaa", reply_markup=reply_language)
                    # print('BOT:', select_lang)
                    # Check if query exists and has data attribute

                    # print(data)
                elif text == "📷🧏 Na Madaala":
                    # print('BOT:', text)
                    await update.message.reply_text("mee sadarkaa naaf kenni", reply_markup=reply_rank_or)

                # come back here
                elif text == '💬 Yaada':
                    # Start the comment conversation
                    await start_comment(update, context)
                   
                elif text == 'Chaanaalii Michu':
                    db.michuChannel(chat_ids, lang_id[chat_ids])
                    await update.message.reply_text('Chaanaalii michu kunooti, ​​hawaasa keenya nu waliin ta\'aa 👇👇👇 \n https://t.me/michudigitallending')

                else:
                    payload = {
                        'sender': message_type,
                        'message': text
                    }
                    intent_payload = {"text": text}

                    # Send message to RASA API endpoint to get response
                    r = requests.post(RASA_API_ENDPOINT_or, json=payload)

                    # Indicate typing action to the user
                    await context.bot.send_chat_action(chat_id=chat_ids, action="typing")

                    # Send message to intent recognition endpoint
                    intent = requests.post(
                        INTENT_ENDPOINT_or, json=intent_payload)
                    if intent.status_code == 200:
                        # Extract response from RASA API
                        response = r.json()

                        # Parse intent and confidence score from the response
                        modelIntent = intent.json()['intent']['name']
                        confidence_score = round(intent.json()['intent']['confidence'] if 'confidence' in intent.json()['intent'] else None, 5)

                        # Handle response based on model intent
                        if modelIntent == "greet":
                            respp = response[0]['text'] + \
                                " " + "Mr/Ms" + " " + fristName
                        else:
                            respp = response[0]["text"]

                        # Extract buttons from response
                        buttons = response[0].get('buttons', [])

                        # Check if the model intent is 'FAQ'
                        if modelIntent == 'FAQ':
                            # Create inline keyboard markup for FAQ response
                            keyboard = [[InlineKeyboardButton(
                                button['title'], callback_data=button['payload'])] for button in buttons]
                            reply_markup = InlineKeyboardMarkup(keyboard)

                        else:
                            # Create inline keyboard markup for other responses
                            keyboard = [InlineKeyboardButton(
                                button['title'], callback_data=button['payload']) for button in buttons]
                            reply_markup = InlineKeyboardMarkup([keyboard])

                        # Reply to the user with the message and inline keyboard markup
                        # Print model prediction and confidence
                        # print('BOT:', text)
                        # print('Confidence:', confidence_score)
                        # print(modelIntent)
                        db.botAnswer(chat_ids, lang_id[chat_ids],  modelIntent, respp)
                        db.textQuestion(chat_ids, lang_id[chat_ids], text, modelIntent, confidence_score, respp)
                        await update.message.reply_text(text= respp, reply_markup=reply_markup)
                    else:
                        # Log the error for debugging purposes
                        print("Intent API request failed:", intent.status_code)

                        # Inform the user that there was an issue processing their request
                        error_message = "Sorry, I couldn't process your request at the moment. Please try again later."
                        await update.message.reply_text(error_message)
            elif select_lang == "አማርኛ":
                if text == '🔠 English  ||  Afaan Oromo  ||  አማርኛ':
                    # for row in reply_language.inline_keyboard:
                    #     for button in row:
                    #         print(button.text)
                    # print('BOT:', text)
                    await update.message.reply_text(text="እሺ ቋንቋ መቀየር ትፈልጋላቹ እባክህ የፈለጉትን ቋንቋ ምረጥ", reply_markup=reply_language)
                    # print('BOT:', select_lang)
                    # Check if query exists and has data attribute

                    # print(data)
                elif text == '📷🧏 ደረጃ ሰጡኝ':
                    # print('BOT:', text)
                    await update.message.reply_text("እባክዎን ደረጃ ይስጡኝ", reply_markup=reply_rank_am)
                # come back here
                elif text == '💬 አስተያየት':
                    # Start the comment conversation
                    await start_comment(update, context)
                    # put here the comment code here
                    # here if user clilck the comment button from ReplyKeyboardMarkup it take the user comment and responde thanks lastly

                elif text == 'ሚቹ ቻናል':
                    db.michuChannel(chat_ids, lang_id[chat_ids])
                    await update.message.reply_text('ሚቹ ቻናል ይኸውና ማህበረሰባችንን ይቀላቀሉን።👇👇👇 \n https://t.me/michudigitallending')

                elif text == '🎰 Guide Video':
                    await update.message.reply_text(text='Guide Video is not ready for now')
                else:
                    payload = {
                        'sender': message_type,
                        'message': text
                    }
                    intent_payload = {"text": text}

                    # Send message to RASA API endpoint to get response
                    r = requests.post(RASA_API_ENDPOINT_am, json=payload)

                    # Indicate typing action to the user
                    await context.bot.send_chat_action(chat_id=chat_ids, action="typing")

                    # Send message to intent recognition endpoint
                    intent = requests.post(
                        INTENT_ENDPOINT_am, json=intent_payload)
                    if intent.status_code == 200:
                        # Extract response from RASA API
                        response = r.json()

                        # Parse intent and confidence score from the response
                        modelIntent = intent.json()['intent']['name']
                        confidence_score = round(intent.json()['intent']['confidence'] if 'confidence' in intent.json()['intent'] else None, 5)

                        # Handle response based on model intent
                        if modelIntent == "greet":
                            respp = response[0]['text'] + \
                                " " + "Mr/Ms" + " " + fristName
                        else:
                            respp = response[0]["text"]

                        # Extract buttons from response
                        buttons = response[0].get('buttons', [])

                        # Check if the model intent is 'FAQ'
                        if modelIntent == 'FAQ':
                            # Create inline keyboard markup for FAQ response
                            keyboard = [[InlineKeyboardButton(
                                button['title'], callback_data=button['payload'])] for button in buttons]
                            reply_markup = InlineKeyboardMarkup(keyboard)

                        else:
                            # Create inline keyboard markup for other responses
                            keyboard = [InlineKeyboardButton(
                                button['title'], callback_data=button['payload']) for button in buttons]
                            reply_markup = InlineKeyboardMarkup([keyboard])

                        # Reply to the user with the message and inline keyboard markup
                        # Print model prediction and confidence
                        # print('BOT:', respp)
                        # print('Confidence:', confidence_score)
                        # print(modelIntent)
                        db.botAnswer(chat_ids, lang_id[chat_ids],  modelIntent, respp)
                        db.textQuestion(chat_ids, lang_id[chat_ids], text, modelIntent, confidence_score, respp)
                        await update.message.reply_text(text= respp, reply_markup=reply_markup)
                    else:
                        # Log the error for debugging purposes
                        # print("Intent API request failed:", intent.status_code)

                        # Inform the user that there was an issue processing their request
                        error_message = "Sorry, I couldn't process your request at the moment. Please try again later."
                        await update.message.reply_text(error_message)
    else:
        resp = 'There have been some improvements to the bot; please select a language first to proceed with the latest one.\n\n Fooyya\'iinsi tokko tokko bot kana irratti waan goodhameef; mee dursa afaan filachuun itti fufaa.\n\n በቦቱ ላይ አንዳንድ ማሻሻያዎች ተደርገዋል; ፤ እባክዎ ቋንቋ መርጠው ይቅጥሉ ።'
        await update.message.reply_text(text=resp, reply_markup=reply_language, parse_mode="Markdown")

# Define a constant for the comment state
COMMENT  = 1
# Define the function to start the comment conversation

async def start_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.from_user.id
    
    if chat_id in lang_button:
        if lang_button[chat_id] == 'አማርኛ':
            await update.message.reply_text('በጣም ጥሩ! እባክዎን አስተያየትዎን አሁን ያስቀምጡ ወይም፣ ለማቆም /cancel ብለው ይተይቡ።')
            return COMMENT
        
        elif lang_button[chat_id] == 'Afaan Oromo':
            await update.message.reply_text("Hayyyee! Amma Yaada keessan naaf erguu dandeessu. adda kutuuf /cancel xuuqi")
            return COMMENT
        
        else:
            await update.message.reply_text('Great! Please put your comment now, or type /cancel to stop.')
            
            return COMMENT
        
    else:
        resp = 'There have been some improvements to the bot; please select a language first to proceed with the latest one.\n\n Fooyya\'iinsi tokko tokko bot kana irratti waan goodhameef; mee dursa afaan filachuun itti fufaa.\n\n በቦቱ ላይ አንዳንድ ማሻሻያዎች ተደርገዋል; ፤ እባክዎ ቋንቋ መርጠው ይቅጥሉ ።'
        await update.message.reply_text(text=resp, reply_markup=reply_language, parse_mode="Markdown")
        return ConversationHandler.END


# Define the function to handle user's input during the comment conversation

async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the chat_id and user_input
    user_id = update.message.from_user.id
    user_input = update.message.text
    
    if user_id in lang_button:
        if user_input == '/cancel':
            if lang_button[user_id] == 'አማርኛ':
                await update.message.reply_text('መልካም! አንድ ቀን አስተያየት እንደምትሰጡኝ ተስፋ አደርጋለሁ')
            elif lang_button[user_id] == 'Afaan Oromo':
                await update.message.reply_text('Tole! Guyya biraa yaada akka naaf laattan abdiin qaba')
            else:
                await update.message.reply_text('Good! I hope you will give me a comment one day.')
        else:
            # Store comment 
            db.userComment(user_id, lang_id[user_id], user_input)
            if lang_button[user_id] == 'አማርኛ':
                await update.message.reply_text(' አመሰግናለው በአስተያየቶ መሰረት እሰራለሁ')
            elif lang_button[user_id] == 'Afaan Oromo':
                await update.message.reply_text('Galatooma yaada keessan irrattan hojjadha')
            else:
                await update.message.reply_text('Thank you! I will work on your comment!')
    else:
        await update.message.reply_text('Please choose a language first.')
    
    return ConversationHandler.END
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Define the conversation handler for comments
comment_handler = ConversationHandler(
    entry_points=[MessageHandler(
        filters.Regex('^💬 (Comment|Yaada|አስተያየት)$'), start_comment)],
    states={
        COMMENT: [MessageHandler(filters.TEXT, comment)],
        
    },
    fallbacks=[]
)

# Set up conversation handler
dev_handler = ConversationHandler(
    entry_points=[CommandHandler('dev', dev)],
    states={
        EMAIL: [MessageHandler(filters.TEXT, email_handler)],
        SUGGETION: [MessageHandler(filters.TEXT, suggetion_handler)],
    },
    fallbacks=[]
)

if __name__ == '__main__':
    print('starting bot ....')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about_command))
    # Add conversation handler to the dispatcher
    app.add_handler(dev_handler)
    app.add_handler(comment_handler)

    # message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Callback query handler
    app.add_handler(CallbackQueryHandler(handle_button_click))

    # Errors
    app.add_error_handler(error)

    # polls the bot
    print('polling ...')

    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)
