from repository.logging_bot import logging_bot, log_function_call
import inspect  # use for getting name func

class VocabularyService:
    def __init__(self, connection):
        self.conn = connection

    @log_function_call
    def get_vocabulary(self):
        try:
            vocabulary = {}
            cur = self.conn.cursor()
            cur.execute(
                """SELECT id, word_en, word_ru, description, flag_repeat, time_request
                FROM auto_repeat_tgbot_eng
                WHERE time_request < now() OR time_request IS NULL
                ORDER BY id LIMIT 5"""
            )
            rows_ = cur.fetchall()
            key_en = 0
            for i in rows_:
                key_en += 1
                vocabulary[key_en] = i
            return vocabulary
        except Exception as ex:
            logging_bot.error(f"Exception in method '{self.__class__.__name__}."
                              f"{inspect.currentframe().f_code.co_name}': {ex}")

    @log_function_call
    def update_word_repeat(self, flag_repeat, word_id, intervals, reset=False):
        try:
            cur = self.conn.cursor()
            if reset:
                cur.execute(
                    """UPDATE auto_repeat_tgbot_eng  
                    SET time_request = NULL, flag_repeat = 0
                    WHERE id = %s""", (int(word_id),)
                )
            else:
                cur.execute(
                    """UPDATE auto_repeat_tgbot_eng  
                    SET time_request = CURRENT_TIMESTAMP + interval %s, flag_repeat = flag_repeat + 1
                    WHERE id = %s""", (str(intervals[flag_repeat]), int(word_id))
                )
            return f"SUCCESS"
        except Exception as ex:
            logging_bot.error(f"Exception in method '{self.__class__.__name__}."
                              f"{inspect.currentframe().f_code.co_name}': {ex}")

    @log_function_call
    def add_word_repository(self, new_word_en, new_word_ru, new_description):
        try:
            cur = self.conn.cursor()
            cur.execute(
                """INSERT INTO auto_repeat_tgbot_eng (word_en, word_ru, description)
                   VALUES (%s, %s, %s)""", (new_word_en, new_word_ru, new_description)
            )
            return f"SUCCESS"
        except Exception as ex:
            logging_bot.error(f"Exception in method '{self.__class__.__name__}."
                              f"{inspect.currentframe().f_code.co_name}': {ex}")