from genericpath import exists, isfile
from http.client import GONE
from lib2to3.pgen2.token import NAME
import os, sys, random, webbrowser
from tkinter import E
from typing import Optional
from datetime import datetime
from time import sleep
from pynput import keyboard
from pynput.mouse import Controller as MouseController
from cryptography.fernet import Fernet

#Language sets
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
    "what_do_you_wanna_do": "What do you want to do?\n->   1. Make a new diary log\n->   2. Read a diary log\n->   3. Remove all previous diary logs\n->   4. Remove a diary log\n->   5. Rate the diary\n->   6. Exit\n",
    "what_do_you_wanna_do_answers": ["1", "2", "3", "4", "5", "6"],
    "oki_dockie": "Okie dockie. Write everything here. At the end write '(end)' and press Enter",
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
    "what_do_you_wanna_do": "Что Вы хотите сделать?\n->   1. Создать новую запись\n->   2. Прочитать запись\n->   3. Удалить все предыдущие записи\n->   4. Удалить одну запись\n->   5. Оценить приложение\n->   5. Выйти\n",
    "what_do_you_wanna_do_answers": ["1", "2", "3", "4", "5", "6"],
    "oki_dockie": "Окей. Пишите все сюда. В конце напишите '(конец)' и нажмите Enter",
    "end_of_log": "(конец)",
    "log_deleted": "Запись удалена",
    "log_which_delete": "Какую запись из дневника Вы хотите удалить?",
    "log_which_read": "Какую запись из дневника вы хотите прочитать?",
    "deleting_all_logs": "Удаляю все записи из дневника...",
    "all_logs_deleted": "Все записи теперь безвозвратно удалены",
    "hundred_percent_sure": "Похоже что Вы 100% уверены..."
}
LANGUAGES_SETS = {
    "en": ENGLISH_LANGUAGE_SET,
    "ru": RUSSIAN_LANGUAGE_SET
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
i_didnt_understand = [""]
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

DIARY_NAME = ".Diary"
DIARY_PARENT_FOLDER = os.path.expanduser("~/")
DIARY_PATH = DIARY_PARENT_FOLDER + DIARY_NAME
CONFIGURATIONS_FILENAME = ".Configurations.txt"
CONFIGURATIONS_PATH = DIARY_PATH + "/" + CONFIGURATIONS_FILENAME
KEY_FILE_NAME = ".Key.key"
KEY_PARENT_FOLDER_OF_PARENT_FOLDER = os.path.expanduser("~/")
KEY_FOLDER_NAME = ".Configs008"
KEY_FOLDER_PATH = KEY_PARENT_FOLDER_OF_PARENT_FOLDER + "/" + KEY_FOLDER_NAME
KEY_PATH = KEY_PARENT_FOLDER_OF_PARENT_FOLDER + "/" + KEY_FILE_NAME
GO_BACK_IN_MENU = False

def createFolderIfDoesntExists(parentFolder, folder):
    os.chdir(parentFolder)
    if not os.path.exists(folder): os.mkdir(folder)

createFolderIfDoesntExists(DIARY_PARENT_FOLDER, DIARY_NAME)
createFolderIfDoesntExists(KEY_PARENT_FOLDER_OF_PARENT_FOLDER, KEY_FOLDER_NAME)


#Format for Configurations.txt
#    0             1          2        3          4
#[PASSWORD|REQUIRE_PASSWORD|NAMES|NAMES_ASKING|LANGUAGE]
PASSWORD = ""
REQUIRE_PASSWORD = True
NAMES = []
LANGUAGE = "en"

LOCKED = True
def setTitlesComparingToLanguage(LanguageSet: dict):
    global please_write_password, saving_your_log, log_successfully_saved, log_made_at, log_noun, error_occured_while_saving_log, error_occured_while_saving_log_answers, exit_continue_stop, keyboard_stop_logging, keyboard_continue_logging, i_didnt_understand, can_you_repeat, heres_your_log, appOrKeyboard, appOrKeyboardAnswers, are_you_sure, are_you_sure_answers, there_are_no_logs, what_do_you_wanna_do, what_do_you_wanna_do_answers, oki_dockie, log_deleted, log_which_read, log_which_delete, deleting_all_logs, all_logs_deleted, hundred_percent_sure, end_of_log

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
def wr(text: str):
    print("-> " + text)

keyboardListenedText = ""
monitorKeyboard = True
command = ""
waitingForCommand = False

#Logs functions
def findAllLogs():
    global DIARY_PATH, CONFIGURATIONS_FILENAME
    logs = []
    os.chdir(os.path.expanduser(DIARY_PATH))
    for el in os.listdir():
        if isfile(el) and el.endswith(".txt") and el != "" and el != CONFIGURATIONS_FILENAME: logs.append(el)
    return logs

def log(text: str):
    global DIARY_PATH, log_made_at, log_noun

    now = datetime.now()
    path = "{diaryPath}/{day}-{month}-{year}.txt".format(diaryPath=os.path.expanduser(DIARY_PATH), day=now.strftime("%d"), month=now.strftime("%m"), year=now.strftime("%Y"))
    
    previousLogs = ""
    try: previousLogs = decrypt(open(path, "rb").read())
    except: pass
    file = open(path, "ba")
    content = previousLogs + "\n+\n{log_made} {local_time} {local_time_compared_to_UTC}\n{logNoun}:\n{log}\n+\n".format(log_made=log_made_at, local_time=now.strftime("%X"), local_time_compared_to_UTC=now.strftime("%z"), log=text, logNoun=log_noun)
    file.write(encrypt(content))
    file.close()

def readDiaryLog():
    global DIARY_PATH, there_are_no_logs, heres_your_log, log_which_read, GO_BACK_IN_MENU
    logs = findAllLogs()
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
    if GO_BACK_IN_MENU: return
    with open(logs[int(answ) - 1], "rb") as f:
        print(heres_your_log)
        print(decrypt(f.read()))

def makeNewDiaryLog():
    global keyboardListenedText, appOrKeyboardAnswers, appOrKeyboard, oki_dockie, end_of_log, GO_BACK_IN_MENU
    answer = ask(question=appOrKeyboard + "\n", answers=appOrKeyboardAnswers)
    if GO_BACK_IN_MENU: return
    if answer == appOrKeyboardAnswers[0]: 
        wr(oki_dockie)
        logText = ""
        finished = False

        while not finished:
            lineOfText = input()
            if lineOfText == end_of_log: finished = True
            else: logText += lineOfText + "\n"

        try: saveLog(logText)
        except: someErrorOccuredWhileSavingYourLog(logText)
    elif answer == appOrKeyboardAnswers[1]: 
        try: listenToKeyboard_makeNewLog()
        except: saveLog(keyboardListenedText)

def saveLog(logText: str):
    global saving_your_log, log_successfully_saved
    wr(saving_your_log)
    log(logText)
    wr(log_successfully_saved)

def removeDiaryLog():
    global DIARY_PATH, are_you_sure, are_you_sure_answers, heres_your_log, there_are_no_logs, log_deleted, log_which_delete, GO_BACK_IN_MENU
    logs = findAllLogs()
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
    if GO_BACK_IN_MENU: return
    are_you_sure_answer = ask(question=are_you_sure + "\n", answers=are_you_sure_answers)
    if GO_BACK_IN_MENU: return

    if are_you_sure_answer == are_you_sure_answers[0]:
        filename = logs[int(answ) - 1]
        with open(filename, "rb") as f:
            wr(heres_your_log + "\n")
            print(decrypt(f.read()))
        os.remove(filename)
        wr(log_deleted)

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

#Encryption-Decryption functions
def encrypt(text: str):
    key = getKey()
    content_bytes = text.encode()
    return Fernet(key).encrypt(content_bytes)

def decrypt(content: bytes):
    key = getKey()
    content_bytes = Fernet(key).decrypt(content)
    return content_bytes.decode()

def getKey():
    global KEY_PATH
    return open(KEY_PATH, "rb").read()

#Errors handling functions
def someErrorOccuredWhileSavingYourLog(logText: str):
    global error_occured_while_saving_log, error_occured_while_saving_log_answers, log_successfully_saved, heres_your_log, GO_BACK_IN_MENU

    answer = ask(question=error_occured_while_saving_log, answers=error_occured_while_saving_log_answers)
    if GO_BACK_IN_MENU: return
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

def sorry_i_didnt_understand(askToDoAnotherTime = True):
    """
    Prints 'I didn't understand' texts with names from NAMES and NAMES_ASKING
    """
    global NAMES, i_didnt_understand, can_you_repeat

    if random.randint(a=0, b=1) == 1 or NAMES == []:
        i_didnt_understand_phrase = random.choice(i_didnt_understand) + ". "
    else: 
        i_didnt_understand_phrase = random.choice(i_didnt_understand) + ", {name}. ".format(name=random.choice(NAMES)) + ". "

    can_you_repeat_phrase = random.choice(can_you_repeat)

    if askToDoAnotherTime:  
        wr(i_didnt_understand_phrase + can_you_repeat_phrase)
    else: 
        wr(i_didnt_understand_phrase)

#Other functions
def destroyDiary():
    """
    Destroys all diary logs permanently. Recommened to enable this feature only with confirming password.
    """
    global DIARY_PATH

    os.chdir(DIARY_PATH)
    logs = findAllLogs()
    for log in logs: os.remove(log)
    
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

def ask(question: str, answers):
    """
    Equals input(question), but if user writes an answer that is not in the array answers, the function i_didnt_understand() will be called. And so on untill the user gives an answer from the array answers.
    """
    answ = ""
    understood = False

    while not understood:
        answ = input("-> " + question)
        if answ == "exit": 
            GO_BACK_IN_MENU = True
            understood = True
        for el in answers:
            if answ == el: 
                understood = True
                break
        if not understood: sorry_i_didnt_understand()
    return answ

def exit():
    """
    Stops all processes and quits the application
    """
    sys.exit(0)

def setup():
    global LANGUAGES_SETS, LANGUAGE, PASSWORD, REQUIRE_PASSWORD, NAMES, CONFIGURATIONS_PATH, KEY_PATH
    wr("Please choose language:")
    question = ""
    for key in LANGUAGES_SETS.keys():
        question += "-> " + key + "\n"
    LANGUAGE = ask(question=question, answers=LANGUAGES_SETS.keys())
    setTitlesComparingToLanguage(LANGUAGES_SETS[LANGUAGE])
    
    wr("Welcome in your personal diary! (Press Enter to continue)")
    input()
    wr("It was designed to provide you security and comfort while storing your secrets.")
    input()
    wr("Let's start setup!")
    input()

    #Setup PASSWORD
    REQUIRE_PASSWORD = True
    if ask(question="Would you like to setup password to access the programm?(y/n)\n", answers=["y", "n"]) == "y":
        PASSWORD = input("-> Please write your password:\n")
        wr("Your password is succesfully saved!")
    else: 
        wr("No problem! You won't need your password to sign in, but you have to set it anyway to be able to, for example, fully destroy your diary, change the password or language")
        PASSWORD = input("-> Please write your password:\n")
        REQUIRE_PASSWORD = False
        wr("Your password is succesfully saved!")
    input()

    #Setup NAMES
    if ask(question="Would you like to provide information how I should call you?(y/n)\n", answers=["y", "n"]) == "y":
        wr("Okay. Now write the names you would like me to call you separated with a line and at the last line write '&end&:")
        ended = False
        while not ended:
            text = input()
            if text == "&end&": ended = True
            else: NAMES.append(input().strip())
        wr("Super! I saved your names, but you can change them anytime, " + random.choice(NAMES))
    input()
    with open(CONFIGURATIONS_PATH, "ba") as file:
        #Format for Configurations.txt
        #   0             1          2       4
        #PASSWORD|REQUIRE_PASSWORD|NAMES|LANGUAGE

        content = "{passw}|{req_passw}|".format(passw = PASSWORD, req_passw = REQUIRE_PASSWORD)

        for index, name in enumerate(NAMES): 
            if index + 1 == len(NAMES): content += name + "|"
            else: content += name + ","
        
        content += LANGUAGE
        key = Fernet.generate_key()
        with open(KEY_PATH, "ba") as keyFile:
            keyFile.write(key)
        file.write(encrypt(content))
    REQUIRE_PASSWORD = False
    wr("Now your setup is done. Don't forget to write 'exit' anytime you want to exit.")

def rateTheApp():
    pathToRateTheApp = "https://forms.gle/f1amtEK3BcnVuUh89"
    webbrowser.open(pathToRateTheApp)

def fromStrToBool(text: str):
    if text == "False" or "false": return False
    elif text == "True" or "true": return True
    else: Exception("String '" + text + "' can't be converted to type Boolean")

#------------------START------------------

if exists(CONFIGURATIONS_PATH):
    with open(CONFIGURATIONS_PATH, "rb") as f:
        content = decrypt(f.read())
        configurations = content.split("|")
        if len(configurations) == 4:
            PASSWORD = configurations[0]
            REQUIRE_PASSWORD = fromStrToBool(configurations[1])
            NAMES = configurations[2].split(",")
            LANGUAGE = configurations[3]
        elif len(configurations) == 3:
            PASSWORD = configurations[0]
            REQUIRE_PASSWORD = fromStrToBool(configurations[1])
            LANGUAGE = configurations[2]
            setTitlesComparingToLanguage(LANGUAGES_SETS[LANGUAGE])
else: 
    setup()
    input()

while True:
    if REQUIRE_PASSWORD:
        while LOCKED:
            print("LOCKED")
            passw = input(please_write_password)
            if not lockOrUnlock(passw): sorry_i_didnt_understand()
    GO_BACK_IN_MENU = False
    answer = ask(question=what_do_you_wanna_do, answers=what_do_you_wanna_do_answers)
    if GO_BACK_IN_MENU: continue
    if answer == what_do_you_wanna_do_answers[0]: 
        makeNewDiaryLog()
        input()
    elif answer == what_do_you_wanna_do_answers[1]: 
        readDiaryLog()
        input()
    elif answer == what_do_you_wanna_do_answers[2]:
        LOCKED = True
        if lockOrUnlock(input(please_write_password)): 
            answ = ask(question=are_you_sure + "\n", answers=are_you_sure_answers)
            if GO_BACK_IN_MENU: continue
            if answ == are_you_sure_answers[0]:
                wr(hundred_percent_sure)
                sleep(1)
                wr(deleting_all_logs)
                destroyDiary()
                sleep(1)
                wr(all_logs_deleted)
            else: continue
        else: sorry_i_didnt_understand(askToDoAnotherTime=False)
    elif answer == what_do_you_wanna_do_answers[3]:  removeDiaryLog()
    elif answer == what_do_you_wanna_do_answers[4]: rateTheApp()
    elif answer == what_do_you_wanna_do_answers[5]: exit()