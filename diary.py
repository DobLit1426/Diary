from genericpath import isfile
import os, sys, random
from datetime import datetime
from time import sleep
from pynput import keyboard
from pynput.mouse import Controller as MouseController

DIARY_PATH = "~/.Diary"
CONFIGURATIONS_FILE_NAME = "Configurations.txt"
CONFIGURATIONS_PATH = DIARY_PATH.join(CONFIGURATIONS_FILE_NAME)
KEY_FILE_NAME = "Key.key"
KEY_PATH = DIARY_PATH.join(KEY_FILE_NAME)
NAMES = ["Your Majesty", "Dobromir", "Mister Litvinov"]
NAMES_ASKING = ["You"]
LANGUAGE = "ru"
ENGLISH_LANGUAGE_SET = {
    "please_write_password": "-> Please write the password to access the function:\n",
    "saving_your_log": "Saving your log...",
    "log_successfully_saved": "I successfully saved your log!",
    "heres_your_log": "Here is your diary log:",
    "log_made_at": "Log made at",
    "log_noun": "Log",
    "error_occured_while_saving_log": "Oops! Some error occured while saving Your log.\n-> Should I try again or show you your log, so you can copy it?\n-> Or do you wanna destroy it?\n->(try/show/destr)",
    
    #IMPORTANT! "error_occured_while_saving_log_answers" must be in order ["try", "show", "destr"]
    "error_occured_while_saving_log_answers": ["try", "show", "destr"],

    "exit_continue_stop": ["exit", "continue", "stop"],
    "keyboard_stop_logging": "Keyboard stop logging",
    "keyboard_continue_logging": "Keyboard continue logging",

    "i_didnt_understand": ["I didn't quite understand", "I am so sorry, but I didn't hear You"],
    "can_you_repeat": ["Could You please repeat?", "Can you say it please another time?"],

    "appOrKeyboard": "Do you want to write the log in the app or listen to the keyboard?(app/keyb)",
    "appOrKeyboardAnswers": ["app", "keyb"],
    "are_you_sure": "Are you sure about that?\n-> There's no way back.\n-> (sure/back)",
    "are_you_sure_answers": ["sure", "back"],
    "there_are_no_logs": "There are currently no diary logs.",
    "what_do_you_wanna_do": "What do you want to do?\n->   1. Make a new diary log\n->   2. Read a diary log\n->   3. Remove all previous diary logs\n->   4. Remove a diary log\n->   5. Exit\n",
    "what_do_you_wanna_do_answers": ["1", "2", "3", "4", "5"],
    "oki_dockie": "Okie dockie. Write everything here. At the end write '&end&' and press Enter",
    "log_deleted": "The log is successfully deleted",
    "log_which_delete": "Which log do you wanna delete?",
    "log_which_read": "Which log do you wanna read?",
    "deleting_all_logs": "Deleting all logs...",
    "all_logs_deleted": "All logs are now permanently deleted",
    "hundred_percent_sure": "Looks like you are 100% sure...",
    "end_of_log": "(end)",
}

RUSSIAN_LANGUAGE_SET = {
    "please_write_password": "-> Пожалуйста напишите пароль, чтобы получить доступ к этой программе:\n",
    "saving_your_log": "Сохраняю вашу запись...",
    "log_successfully_saved": "Я сохранил вашу запись!",
    "heres_your_log": "Вот ваша запись из дневника:",
    "log_made_at": "Запись сделана",
    "log_noun": "Запись",
    "error_occured_while_saving_log": "Упс! Какая-то ошибка возникла, пока я пытался сохранить вашу записб.\n-> Попробовать еще раз или показать вашу запись, так что вы сможете ее скопировать?\n-> Или Вы хотите уничтожить запись?\n->(попытаться/показать/уничтожить)",
    
    #IMPORTANT! "error_occured_while_saving_log_answers" must be in order ["try", "show", "destr"]
    "error_occured_while_saving_log_answers": ["попытаться", "показать", "уничтожить"],

    "exit_continue_stop": ["выйти", "продолжить", "остановиться"],
    "keyboard_stop_logging": "Перестать записывать",
    "keyboard_continue_logging": "Продолжить записывать",

    "i_didnt_understand": ["Я не совсем понял", "Простите, я вас плохо слышу"],
    "can_you_repeat": ["Не могли бы Вы повторить?", "Не могли бы Вы сказать еще раз?"],

    "appOrKeyboard": "Хотите ли Вы писать запись в приложении или считывать нажатия клавиатуры?(прил/клав)",
    "appOrKeyboardAnswers": ["прил", "клав"],
    "are_you_sure": "Вы уверены насчет этого?\n-> Все записи будут удалены безвозвратно.\n-> Пути назад не будет.\n->(уверен/назад)",
    "are_you_sure_answers": ["уверен", "назад"],

    "there_are_no_logs": "В настоящий момент никаких дневниковых записей нет",
    "what_do_you_wanna_do": "Что Вы хотите сделать?\n->   1. Создать новую запись\n->   2. Прочитать запись\n->   3. Удалить все предыдущие записи\n->   4. Удалить одну запись\n->   5. Выйти\n",
    "what_do_you_wanna_do_answers": ["1", "2", "3", "4", "5"],
    "oki_dockie": "Окей. Пишите все сюда. В конце напишите '(конец)' и нажмите Enter",
    "end_of_log": "(конец)",
    "log_deleted": "Запись удалена",
    "log_which_delete": "Какую запись из дневника Вы хотите удалить?",
    "log_which_read": "Какую запись из дневника вы хотите прочитать?",
    "deleting_all_logs": "Удаляю все записи из дневника...",
    "all_logs_deleted": "Все записи теперь безвозвратно удалены",
    "hundred_percent_sure": "Похоже что Вы 100% уверены..."
}
please_write_password = ""
saving_your_log = ""
log_successfully_saved = ""
log_made_at = ""
log_noun = ""
log_which_delete = ""
end_of_log = ""
log_which_read = ""
log_deleted = ""
are_you_sure = ""
error_occured_while_saving_log = ""
error_occured_while_saving_log_answers = []
exit_continue_stop = []
keyboard_stop_logging = ""
keyboard_continue_logging = ""
i_didnt_understand = ""
can_you_repeat = []
heres_your_log = ""
appOrKeyboardAnswers = []
appOrKeyboard = ""
are_you_sure_answers = []
there_are_no_logs = ""
what_do_you_wanna_do = ""
what_do_you_wanna_do_answers = []
oki_dockie = ""
deleting_all_logs = ""
all_logs_deleted = ""
hundred_percent_sure = ""

def setTitlesComparingToLanguage(LanguageSet):
    global please_write_password, saving_your_log, log_successfully_saved, log_made_at, log_noun, error_occured_while_saving_log, error_occured_while_saving_log_answers, exit_continue_stop, keyboard_stop_logging, keyboard_continue_logging, i_didnt_hear, i_didnt_understand, can_you_repeat, heres_your_log, appOrKeyboard, appOrKeyboardAnswers, are_you_sure, are_you_sure_answers, there_are_no_logs, what_do_you_wanna_do, what_do_you_wanna_do_answers, oki_dockie, log_deleted, log_which_read, log_which_delete, deleting_all_logs, all_logs_deleted, hundred_percent_sure, end_of_log

    please_write_password = LanguageSet["please_write_password"]
    saving_your_log = LanguageSet["saving_your_log"]
    log_successfully_saved = LanguageSet["log_successfully_saved"]
    log_made_at = LanguageSet["log_made_at"]
    log_noun = LanguageSet["log_noun"]
    error_occured_while_saving_log = LanguageSet["error_occured_while_saving_log"]
    error_occured_while_saving_log_answers = LanguageSet["error_occured_while_saving_log_answers"]
    exit_continue_stop = LanguageSet["exit_continue_stop"]
    keyboard_continue_logging = LanguageSet["keyboard_continue_logging"]
    keyboard_stop_logging = LanguageSet["keyboard_stop_logging"]
    i_didnt_understand = LanguageSet["i_didnt_understand"]
    can_you_repeat = LanguageSet["can_you_repeat"]
    heres_your_log = LanguageSet["heres_your_log"]
    appOrKeyboard = LanguageSet["appOrKeyboard"]
    appOrKeyboardAnswers = LanguageSet["appOrKeyboardAnswers"]
    are_you_sure = LanguageSet["are_you_sure"]
    are_you_sure_answers = LanguageSet["are_you_sure_answers"]
    there_are_no_logs = LanguageSet["there_are_no_logs"]
    what_do_you_wanna_do = LanguageSet["what_do_you_wanna_do"]
    what_do_you_wanna_do_answers = LanguageSet["what_do_you_wanna_do_answers"]
    oki_dockie = LanguageSet["oki_dockie"]
    log_deleted = LanguageSet["log_deleted"]
    log_which_delete = LanguageSet["log_which_delete"]
    log_which_read = LanguageSet["log_which_read"]
    deleting_all_logs = LanguageSet["deleting_all_logs"]
    all_logs_deleted = LanguageSet["all_logs_deleted"]
    hundred_percent_sure = LanguageSet["hundred_percent_sure"]
    end_of_log = LanguageSet["end_of_log"]

if LANGUAGE == "en": setTitlesComparingToLanguage(ENGLISH_LANGUAGE_SET)
elif LANGUAGE == "ru": setTitlesComparingToLanguage(RUSSIAN_LANGUAGE_SET)

def wr(text):
    print("-> " + text)

#Format for Configurations.txt
#[
# PASSWORD,
# REQUIRE_PASSWORD,
# NAMES,
# NAMES_ASKING,
# LANGUAGE
# ]

LOCKED = True
PASSWORD = "ImDiet876"
REQUIRE_PASSWORD = False

keyboardListenedText = ""
monitorKeyboard = True
command = ""
waitingForCommand = False

def findAllLogs():
    logs = []
    os.chdir(os.path.expanduser(DIARY_PATH))
    for el in os.listdir():
        if isfile(el) and el.endswith(".txt") and el != "" : logs.append(el)

def destroyDiary():
    """
    Destroys all diary logs permanently. Recommened to enable this feature only with confirming password.
    """
    global DIARY_PATH

    os.chdir(os.path.expanduser(DIARY_PATH))
    for el in os.listdir():
        if isfile(el) and el.endswith(".txt"): os.remove(el)
    

def lockOrUnlock(passwd = ""):
    """
    If unlocked lockes. if locked unlocks. Returns True if unlocked and False if locked.
    """
    global LOCKED, PASSWORD
    if LOCKED and passwd == PASSWORD: 
        LOCKED = False
        return True
    else:
        LOCKED = True
        return False

def sorry_i_didnt_understand(askToDoAnotherTime=True):
    """
    Prints 'I didn't understand' texts with names from NAMES and NAMES_ASKING
    """
    global NAMES_ASKING, NAMES, i_didnt_hear, i_didnt_understand, can_you_repeat

    i_didnt_understand_phrase = random.choice(i_didnt_understand) + (", {name}. ".format(name=random.choice(NAMES) if random.randint(a=0, b=1) == 1 else ". "))
    can_you_repeat_phrase = random.choice(can_you_repeat)

    if askToDoAnotherTime:  wr(i_didnt_understand_phrase + can_you_repeat_phrase)
    else: wr(i_didnt_understand)

def ask(question: str, answers):
    """
    Equals input(question), but if user writes an answer that is not in the array answers, the function i_didnt_understand() will be called. And so on untill the user gives an answer from the array answers.
    """
    answ = ""
    understood = False

    while not understood:
        answ = input("-> " + question)
        for el in answers:
            if answ == el: 
                understood = True
                break
        if not understood: i_didnt_understand()
    return answ

def log(text):
    global DIARY_PATH, log_made_at, log_noun

    now = datetime.now()
    path = "{diaryPath}/{day}-{month}-{year}.txt".format(diaryPath=os.path.expanduser(DIARY_PATH), day=now.strftime("%d"), month=now.strftime("%m"), year=now.strftime("%Y"))
    file = open(path, "a")
    file.write("\n+\n{log_made} {local_time} {local_time_compared_to_UTC}\n{logNoun}:\n{log}\n+\n".format(log_made=log_made_at, local_time=now.strftime("%X"), local_time_compared_to_UTC=now.strftime("%z"), log=text, logNoun=log_noun))
    file.close()


def exit():
    """
    Stops all processes and quits the application
    """
    sys.exit(0)

def someErrorOccuredWhileSavingYourLog(logText):
    global error_occured_while_saving_log, error_occured_while_saving_log_answers, log_successfully_saved, heres_your_log

    answer = ask(question=error_occured_while_saving_log, answers=error_occured_while_saving_log_answers)
    if answer == error_occured_while_saving_log_answers[0]:
        saved = False
        for i in range(1000):
            try: 
                log(logText)
                saved = True
                break
            except: pass
        if saved: wr(log_successfully_saved)
        else: someErrorOccuredWhileSavingYourLog(logText=logText)
    elif answer == error_occured_while_saving_log_answers[1]: 
        wr(heres_your_log + "\n")
        print(logText)
    elif answer == error_occured_while_saving_log_answers[2]: return

def listenToKeyboard_makeNewLog():
    """
    Listens to keyboard and returns the text after typing 7exit7
    """
    global keyboardListenedText, monitorKeyboard, waitingForCommand, command

    keyboardListenedText = ""
    monitorKeyboard = True
    command = ""
    waitingForCommand = False
    def resetCommand():
        global command, waitingForCommand
        waitingForCommand = False
        command = ""

    def succesfulOperation():
        MouseController().position = (0, 0)
        resetCommand()

    def on_press(key):
        global keyboardListenedText, monitorKeyboard, waitingForCommand, command, keyboard_stop_logging, keyboard_continue_logging, exit_continue_stop
        if monitorKeyboard:
            try: keyboardListenedText += key.char
            except AttributeError: 
                if key == keyboard.Key.space: keyboardListenedText += " "
                else: keyboardListenedText += "\_(" + str(key) + ")_/"

        #Command part
        try: 
            specialKey = "7"
            if waitingForCommand == True and key.char == specialKey:
                if command == exit_continue_stop[0]: 
                    raise Exception("")
                elif command == exit_continue_stop[2]:
                    keyboardListenedText += "\_(" + keyboard_stop_logging + ")_/"
                    monitorKeyboard = False
                    succesfulOperation()
                elif command == exit_continue_stop[1]:
                    keyboardListenedText += "\_(" + keyboard_continue_logging + ")_/"
                    monitorKeyboard = True
                    succesfulOperation()
            elif waitingForCommand == True and key.char != specialKey: command += str(key.char)
            elif waitingForCommand == False and key.char == specialKey: waitingForCommand = True
        except AttributeError: resetCommand()
            
    with keyboard.Listener( on_press=on_press ) as listener: listener.join()

def saveLog(logText):
    global saving_your_log, log_successfully_saved
    wr(saving_your_log)
    log(logText)
    wr(log_successfully_saved)


def makeNewDiaryLog():
    global keyboardListenedText, appOrKeyboardAnswers, appOrKeyboard, oki_dockie, end_of_log
    answer = ask(question=appOrKeyboard + "\n", answers=appOrKeyboardAnswers)
        
    if answer == appOrKeyboardAnswers[0]: 
        wr(oki_dockie)
        logText = ""
        finished = False

        while not finished:
            lineOfText = input()
            if lineOfText == end_of_log: finished = True
            else: logText += lineOfText + "\n"

        try: saveLog(logText=logText)
        except: someErrorOccuredWhileSavingYourLog(logText=logText)
    elif answer == appOrKeyboardAnswers[1]: 
        try: listenToKeyboard_makeNewLog()
        except: saveLog(keyboardListenedText)

def removeDiaryLog():
    global DIARY_PATH, are_you_sure, are_you_sure_answers, heres_your_log, there_are_no_logs, log_deleted, log_which_delete
    logs = []
    os.chdir(os.path.expanduser(DIARY_PATH))
    for el in os.listdir():
        if isfile(el) and el.endswith(".txt"): logs.append(el)
    
    if logs == []:
        wr(there_are_no_logs)
        return
    wr(log_which_delete)
    question = ""
    answers = []
    for index, file in enumerate(logs):
        question += "    " + str(index + 1) + ". " + file + "\n"
        answers.append(str(index + 1))

    answ = ask(question=question, answers=answers)
    if ask(question=are_you_sure + "\n", answers=are_you_sure_answers) == are_you_sure_answers[0]:
        filename = logs[int(answ) - 1]
        with open(filename, "r") as f:
            wr(heres_your_log + "\n")
            print(f.read())
            f.close()
        os.remove(filename)
        wr(log_deleted)

def readDiaryLog():
    global DIARY_PATH, there_are_no_logs, heres_your_log, log_which_read
    logs = []
    os.chdir(os.path.expanduser(DIARY_PATH))
    for el in os.listdir():
        if isfile(el) and el.endswith(".txt"): logs.append(el)
    
    if logs == []:
        wr(there_are_no_logs)
        return
    wr(log_which_read)
    question = ""
    answers = []
    for index, file in enumerate(logs):
        question += "    " + str(index + 1) + ". " + file + "\n"
        answers.append(str(index + 1))

    answ = ask(question=question, answers=answers)
    with open(logs[int(answ) - 1], "r") as f:
        print(heres_your_log)
        print(f.read())
    input()


while True:
    if REQUIRE_PASSWORD:
        while LOCKED:
            if not lockOrUnlock(input(please_write_password)): i_didnt_understand()

    answer = ask(question=what_do_you_wanna_do, answers=what_do_you_wanna_do_answers)
    if answer == what_do_you_wanna_do_answers[0]: makeNewDiaryLog()
    elif answer == what_do_you_wanna_do_answers[1]: readDiaryLog()
    elif answer == what_do_you_wanna_do_answers[2]:
        LOCKED = True
        if lockOrUnlock(input(please_write_password)): 
            answ = ask(question=are_you_sure + "\n", answers=are_you_sure_answers)
            if answ == are_you_sure_answers[0]:
                wr(hundred_percent_sure)
                sleep(1)
                wr(deleting_all_logs)
                destroyDiary()
                sleep(1)
                wr(all_logs_deleted)
            else: continue
        else: i_didnt_understand(askToDoAnotherTime=False)
    elif answer == what_do_you_wanna_do_answers[3]: removeDiaryLog()
    elif answer == what_do_you_wanna_do_answers[4]: exit()