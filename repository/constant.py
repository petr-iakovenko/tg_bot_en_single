import service.emj as emj

BUTTON_START = {
    f"{emj.rocket} Let's begin training.": "training",
    f"{emj.question} How does this bot work? (rus)": "about_bot_rus",
    f"{emj.question} How does this bot work? (eng)": "about_bot_eng",
    f"{emj.add_word} Add the word to the vocabulary.": "go_to_add_word_menu"
}

BUTTON_ADDING = {
    f"{emj.question} How to add a new word?": "how_add_pair",
    f"{emj.return_to_menu} Return to the menu.": "back_to_start_menu"

}

BUTTON_ANSWER = {
    f"{emj.light_emj} Get an answer": "answer",
    f"{emj.return_to_menu} Return to the menu.": "back_to_start_menu"
}

BUTTON_DICT = BUTTON_START | BUTTON_ANSWER | BUTTON_ADDING

ABOUT_BOT_RUS = f'should edit - ABOUT_BOT_RUS'
ABOUT_BOT_ENG = f'should edit - ABOUT_BOT_ENG'
HOW_ADD_WORD = f'should edit - HOW_ADD_WORD'

INTERVALS = {
   0 : "10 sec",
   1 : "2 min",
   2 : "10 min",
   3 : "30 min",
   4 : "12 hour",
   5 : "2 day",
   6 : "6 day",
   7 : "13 day",
   8 : "1 month",
   9 : "3 month",
   10 : "6 month"

}

