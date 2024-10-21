import sys
import os
# Добавляем родительский каталог к sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telebot import TeleBot
from repository.logging_bot import log_function_call, logging_bot
# from repository.constant import token, connect_db
from repository.connect import token, connect_db
import service.emj as emj
from service.service_vocabulary import VocabularyService
from service.service_bot import BotService
from repository.constant import (BUTTON_START, BUTTON_ANSWER, ABOUT_BOT_ENG,
                                 ABOUT_BOT_RUS, BUTTON_DICT, HOW_ADD_WORD, INTERVALS)

conn = connect_db()
conn.set_session(autocommit=True)
bot_api = TeleBot(token)

vocabulary_service = VocabularyService(conn)
bot_service = BotService(bot_api, vocabulary_service)


@log_function_call
@bot_api.message_handler(commands=["start"])
def send_welcome(message):
    logging_bot.info(f"Received /start command from chat_id='{message.chat.id}'")
    bot_service.set_chat_id(message.chat.id)
    markup = bot_service.get_button_menu(BUTTON_START)
    bot_api.send_message(
        chat_id=message.chat.id,
        text=f"{emj.run_bot} The bot is running!",
        reply_markup=markup
    )

@log_function_call
@bot_api.message_handler(func=lambda message: message.text in BUTTON_DICT.keys())
def send_info_start(message):
    logging_bot.info(f"Received button command: {message.text} from chat_id='{message.chat.id}'")
    if BUTTON_DICT[message.text] == "training":
        bot_service.send_word()
    elif BUTTON_DICT[message.text] == "about_bot_eng":
        bot_api.send_message(chat_id=message.chat.id, text=ABOUT_BOT_ENG)
    elif BUTTON_DICT[message.text] == "about_bot_rus":
        bot_api.send_message(chat_id=message.chat.id, text=ABOUT_BOT_RUS)
    elif BUTTON_DICT[message.text] == "go_to_add_word_menu":
        bot_api.send_message(chat_id=message.chat.id, text=HOW_ADD_WORD)
    elif BUTTON_DICT[message.text] == "back_to_start_menu":
        markup = bot_service.get_button_menu(BUTTON_START)
        bot_api.send_message(
            chat_id=message.chat.id,
            text=f"{emj.return_to_menu} You are back to menu",
            reply_markup=markup
        )
    elif BUTTON_ANSWER[message.text] == "answer":
        bot_api.send_message(
            chat_id=message.chat.id,
            text=f"{emj.light_emj} Answer: {bot_service.pairs_word['word_en']}"
        )

@log_function_call
@bot_api.message_handler(content_types=['text'])
def get_text_messages(message):
    logging_bot.info(f"Received button command: {message.text} from chat_id='{message.chat.id}'")
    if message.text.lower() == bot_service.pairs_word['word_en']:
        bot_api.send_message(
            chat_id=message.chat.id,
            text=f"{emj.success_emj} Correct!\n{emj.think_emj}"
                 f" Repeating in {INTERVALS[bot_service.pairs_word['flag_repeat']]}"
        )
        vocabulary_service.update_word_repeat(
            flag_repeat=bot_service.pairs_word['flag_repeat'],
            word_id=bot_service.pairs_word['word_id'],
            intervals=INTERVALS
        )
        bot_service.send_word()
    elif "==" in message.text.lower():
        bot_service.add_word(message)
    else:
        bot_api.send_message(
            chat_id=message.chat.id,
            text=f"{emj.fail_emj}You are wrong! \n Answer: {bot_service.pairs_word['word_en']}"
        )
        vocabulary_service.update_word_repeat(
            flag_repeat=bot_service.pairs_word['flag_repeat'],
            word_id=bot_service.pairs_word['word_id'],
            reset=True,
            intervals=INTERVALS[0]
        )
        bot_api.send_message(
            chat_id=message.chat.id,
            text=f"{emj.think_emj} Your interval repeating was reset"
        )
        bot_service.send_word()


bot_api.infinity_polling()