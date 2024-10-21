import random
import inspect  # use for getting name func
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from repository.logging_bot import log_function_call, logging_bot

import service.emj as emj
from repository.constant import BUTTON_START, BUTTON_ANSWER
from service.service_vocabulary import VocabularyService
from repository.connect import token, connect_db

conn = connect_db()
conn.set_session(autocommit=True)
bot_api = TeleBot(token)
vocabulary_service = VocabularyService(conn)

class BotService:
    def __init__(self, bot_api, vocabulary_service):
        self.bot_api = bot_api
        self.vocabulary_service = vocabulary_service
        self.chat_id = ""
        self.pairs_word = {}

    @log_function_call
    def set_chat_id(self, chat_id):
        self.chat_id = chat_id
        return chat_id

    @log_function_call
    def get_vocabulary_words(self):
        try:
            vocabulary = vocabulary_service.get_vocabulary()
            if not vocabulary:
                return None
            else:
                word = random.choice(list(vocabulary.values()))
                return {
                    'word_ru': word[2].lower(),
                    'word_en': word[1].lower(),
                    'word_id': word[0],
                    'counter_word': len(vocabulary),
                    'description': word[3],
                    'flag_repeat': word[4],
                    'time_repeat': word[5],
                }
        except Exception as ex:
            logging_bot.error(f"Exception in method '{self.__class__.__name__}."
                              f"{inspect.currentframe().f_code.co_name}': {ex}")

    @log_function_call
    def send_word(self):
        try:
            self.pairs_word = self.get_vocabulary_words()
            if self.pairs_word is False:
                return self.end_words_error()
            else:
                markup = self.get_button_menu(BUTTON_ANSWER)
                return bot_api.send_message(
                    chat_id=self.chat_id,
                    text=f"{emj.translate_emj} Translate: {self.pairs_word['word_ru'].capitalize()}\n "
                         f"{emj.light_emj}Description: {self.pairs_word['description']}",
                    reply_markup=markup
                )
        except Exception as ex:
            logging_bot.error(f"Exception in method '{self.__class__.__name__}."
                              f"{inspect.currentframe().f_code.co_name}': {ex}")

    @log_function_call
    def end_words_error(self):
        try:
            markup = self.get_button_menu(BUTTON_START)
            return bot_api.send_message(
                chat_id=self.chat_id,
                text=f"{emj.error_emj} Sorry. No words available for repetition.\n"
                f"Please add new words or wait some time",
                reply_markup=markup
            )
        except Exception as ex:
            logging_bot.error(f"Exception in method '{self.__class__.__name__}."
                              f"{inspect.currentframe().f_code.co_name}': {ex}")

    @log_function_call
    def add_word(self, message):
        try:
            word_list = message.text.split('==')
            if len(word_list) != 3:
                bot_api.reply_to(
                    message=message,
                    text=f"{emj.error_emj} Incorrect format. Please send in 'word_en == word_ru == description'."
                )
                return
            new_word_en, new_word_ru, new_description = [word.strip() for word in word_list]
            vocabulary_service.add_word_repository(new_word_en, new_word_ru, new_description)
            return bot_api.reply_to(
                message=message,
                text=f"""{emj.translate_emj}Done! "{new_word_en} - {new_word_ru} - {new_description}"\n"""
                     "- has been added to the vocabulary."
            )
        except Exception as ex:
            logging_bot.error(f"Exception in method '{self.__class__.__name__}."
                              f"{inspect.currentframe().f_code.co_name}': {ex}")

    @log_function_call
    def get_button_menu(self, button_dict):
        try:
            markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            for button in button_dict.keys():
                item_button = KeyboardButton(button)
                markup.add(item_button)
            return markup
        except Exception as ex:
            logging_bot.error(f"Exception in method '{self.__class__.__name__}."
                              f"{inspect.currentframe().f_code.co_name}': {ex}")

    @log_function_call
    def run_answer_menu(self, message):
        try:
            key_button_start = message.text
            value = BUTTON_ANSWER[key_button_start]
            if value == "answer":
                return bot_api.send_message(
                    chat_id=self.chat_id,
                    text=f"{emj.light_emj} Answer: {self.pairs_word['word_en']}"
                )
            elif value == "back_to_start_menu":
                markup = self.get_button_menu(BUTTON_START)
                return bot_api.send_message(
                    chat_id=self.chat_id,
                    text=f"{emj.return_to_menu} Returned to the start menu.",
                    reply_markup=markup
                )
        except Exception as ex:
            logging_bot.error(f"Exception in method '{self.__class__.__name__}."
                              f"{inspect.currentframe().f_code.co_name}': {ex}")