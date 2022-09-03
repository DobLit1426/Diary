from genericpath import isfile
import os, sys, random
from datetime import datetime
from time import sleep
from pynput import keyboard
from pynput.mouse import Controller as MouseController

DIARY_PATH = "~/.Diary"
NAMES = ["Your Majesty", "Dobromir", "Mister Litvinov"]
NAMES_ASKING = ["You"]
LOCKED = True
PASSWORD = "ImDiet876"
REQUIRE_PASSWORD = False

keyboardListenedText = ""
monitorKeyboard = True
command = ""
waitingForCommand = False

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

def i_didnt_understand(askToDoAnotherTime=True):
    """
    Prints 'I didn't understand' texts with names from NAMES and NAMES_ASKING
    """
    global NAMES_ASKING, NAMES
    if askToDoAnotherTime:
        print("-> I didn't quite understand, {name1}. Could {name2} please try again?".format(name1=random.choice(NAMES), name2=random.choice(NAMES_ASKING)))
    else: 
        print("-> I didn't quite understand, {name1}.".format(name1=random.choice(NAMES)))

def ask(question, answers):
    """
    Equals input(question), but if user writes an answer that is not in the array answers, the function i_didnt_understand() will be called. And so on untill the user gives an answer from the array answers.
    """
    answ = ""
    understood = False

    while not understood:
        answ = input(question)
        for el in answers:
            if answ == el: 
                understood = True
                break
        if not understood: i_didnt_understand()
    return answ

def log(text):
    global DIARY_PATH

    now = datetime.now()
    file = open(os.path.expanduser(DIARY_PATH + "/" + now.strftime("%d") + now.strftime("%m") + "-" + now.strftime("%Y") + ".txt"), "a")
    file.write("\n+\nLog made at " + now.strftime("%X") + now.strftime("%z") + "\nLog:\n"+ text + "\n+\n")
    file.close()


def exit():
    """
    Stops all processes and quits the application
    """
    sys.exit(0)

def someErrorOccuredWhileSavingYourLog(logText):
    answer = ask(question="-> Oops! Some error occured while saving Your log.\n-> Should I try again or show you your log, so you can copy it?\n-> Or do you wanna destroy it?\n->(try/show/destr)", answers=["try", "show", "destr"])
    if answer == "try":
        saved = False
        for i in range(1000):
            try: 
                log(logText)
                saved = True
                break
            except: pass
        if saved: print("I successfully saved your log!")
        else: someErrorOccuredWhileSavingYourLog()
    elif answer == "show": 
        print("-> Here's your diary log")
        print(logText)

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
        global keyboardListenedText, monitorKeyboard, waitingForCommand, command
        if monitorKeyboard:
            try: keyboardListenedText += key.char
            except AttributeError: 
                if key == keyboard.Key.space: keyboardListenedText += " "
                else: keyboardListenedText += "\_(" + str(key) + ")_/"

        #Command part
        try: 
            specialKey = "7"
            if waitingForCommand == True and key.char == specialKey:
                if command == "exit": 
                    raise Exception("-> Keyboard stopped listening")
                elif command == "stop":
                    keyboardListenedText += "\_(Keyboard stop logging)_/"
                    monitorKeyboard = False
                    succesfulOperation()
                elif command == "cont":
                    keyboardListenedText += "\_(Keyboard continue logging)_/"
                    monitorKeyboard = True
                    succesfulOperation()
            elif waitingForCommand == True and key.char != specialKey: command += str(key.char)
            elif waitingForCommand == False and key.char == specialKey: waitingForCommand = True
        except AttributeError: resetCommand()
            
    with keyboard.Listener( on_press=on_press ) as listener: listener.join()

def saveLog(logText):
    print("-> Saving your log...")
    try: 
        log(logText)
        print("-> I successfully saved your log!")
    except: someErrorOccuredWhileSavingYourLog(logText=logText)


def makeNewDiaryLog():
    global keyboardListenedText
    answer = ask(question="-> Do you want to write the log in the app or listen to the keyboard?(app/keyb)\n", answers=["app", "keyb"])
        
    if answer == "app": 
        print("-> Okie dockie. Write everything here. At the end write '&end&' and press Enter.")
        logText = ""
        finished = False

        while not finished:
            lineOfText = input()
            if lineOfText == "&end&": finished = True
            else: logText += lineOfText + "\n"

        saveLog(logText=logText)

    elif answer == "keyb": 
        try: listenToKeyboard_makeNewLog()
        except: saveLog(keyboardListenedText)

def removeDiaryLog():
    global DIARY_PATH
    logs = []
    os.chdir(os.path.expanduser(DIARY_PATH))
    for el in os.listdir():
        if isfile(el) and el.endswith(".txt"): logs.append(el)
    
    if logs == []:
        print("-> There are currently no diary logs")
        return
    print("-> Which log do you wanna delete?")
    question = ""
    answers = []
    for index, file in enumerate(logs):
        question += "->    " + str(index + 1) + ". " + file + "\n"
        answers.append(str(index + 1))

    answ = ask(question=question, answers=answers)
    print("-> This action can't be undone")
    if ask(question="-> Are you sure about that?(y/n)\n", answers=["y", "n"]) == "y":
        filename = logs[int(answ) - 1]
        with open(filename, "r") as f:
            print("-> Here is the content of the log:\n")
            print(f.read())
            f.close()
        os.remove(filename)
        print("-> The log is successfully deleted.")

def readDiaryLog():
    global DIARY_PATH
    logs = []
    os.chdir(os.path.expanduser(DIARY_PATH))
    for el in os.listdir():
        if isfile(el) and el.endswith(".txt"): logs.append(el)
    
    if logs == []:
        print("-> There are currently no diary logs")
        return
    print("-> Which log do you wanna read?")
    question = ""
    answers = []
    for index, file in enumerate(logs):
        question += "->    " + str(index + 1) + ". " + file + "\n"
        answers.append(str(index + 1))

    answ = ask(question=question, answers=answers)
    with open(logs[int(answ) - 1], "r") as f:
        print(f.read())


while True:
    if REQUIRE_PASSWORD:
        while LOCKED:
            if not lockOrUnlock(input("-> Please write the password to access the programm:\n")): i_didnt_understand()

    answer = ask(question="-> What do you want to do?\n->   1. Make a new diary log\n->   2. Read a diary log\n->   3. Remove all previous diary logs\n->   4. Remove a diary log\n->   5. Exit\n", answers=["1", "2", "3", "4", "5"])
    if answer == "1": makeNewDiaryLog()
    elif answer == "2": readDiaryLog()
    elif answer == "3":
        LOCKED = True
        if lockOrUnlock(input("-> Please write the password to access the function:\n")): 
            answ = ask(question="-> Are you sure about that?\n-> All logs will be deleted permanently.\n-> There's no way back.\n->(sure/back)\n", answers=["sure", "back"])
            if answ == "sure":
                print("-> Okay, it looks like you are 100% sure.")
                sleep(2)
                print("-> Deleting all your logs...")
                destroyDiary()
                print("-> The diary is destroyed.")
        else: i_didnt_understand(askToDoAnotherTime=False)
    elif answer == "4": removeDiaryLog()
    elif answer == "5": exit()