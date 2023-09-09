# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import datetime as dt
import smtplib
from typing import Any, Text, Dict, List, Union
# from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
# from telegram import Update 
# from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
# from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
# from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton

class actiontime(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now().strftime('%d-%m-%Y  %I:%M:%S  %p')}")

        return []


# class ActionShowImage(Action):
#     def name(self) -> Text:
#         return "action_show_image"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         image_path = "imagee/guyyaa_proccess.png"  # Replace with the actual path to your image

#         # Generate the HTML code to display the image
#         image_html = f"<img src='{image_path}' alt='Image' width='300'>"

#         # Send the HTML code as a message to the user
#         dispatcher.utter_message(text=image_html, parse_mode="HTML")

#         return []








class ActionFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I apologise for not understanding. Could you please rephrase that? \nAlternatively, if you prefer another language, please select it from the keyboard button below.")
        return []

class ActionamFallback(Action):
    def name(self) -> Text:
        return "actionam_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="ይቅርታ፣ አልገባኝም። እባክዎን እንደገና መግለጽ ይችላሉ? እንደአማራጭ፣ ሌላ ቋንቋ ከመረጡ፣ እባክዎን ከታች ካለው የቁልፍ ሰሌዳ በመንካት ይምረጡት።")
        return []
    
class ActionorFallback(Action):
    def name(self) -> Text:
        return "actionor_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hubachuu dhabuu kootiif dhiifama gaafadha. Mee irra deebitee ibsuu dandeessaa? Akka filannootti, afaan biraa yoo barbaadee, button keyboard armaan gadii xuquun filachuu dandeessa.")
        return []