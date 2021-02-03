import datetime
import time
import os
import threading
import json
from msvcrt import getch
from playsound import playsound
from typing import Dict, List


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pressSpaceToContinue():
    print("Press [Space] to continue...\n")
    while 1:
        if getch().decode("utf-8") == " ":
            clear_screen()
            break


def createAlarm(alarms: List):
    title = ""
    alarmMinute = 0
    alarmHour = 0
    repeating = True
    print("You will type in the title, hour(0-23), minute(0-59) and do you want to repeat\n")

    while 1:

        title = input("Title: ")

        while 1:
            try:
                alarmHour = int(input("Hour: "))
                if not (alarmHour > -1 and 24 > alarmHour):
                    raise ValueError
                break
            except ValueError:
                print("Your input is not valid. Please try again")

        while 1:
            try:
                alarmMinute = int(input("Minute: "))
                if not (alarmMinute > -1 and 60 > alarmMinute):
                    raise ValueError
                break
            except ValueError:
                print("Your input is not valid. Please try again")

        while 1:
            repeating = input("Repeat?(y/n) ").lower()
            if repeating not in ['y', 'n']:
                print("Your input is not valid. Please try again")
            else:
                break

        print()

        print("Title:", title)
        print("Time: " + str(alarmHour) + " " + str(alarmMinute) + "hrs")
        print("Repeatable:", repeating)

        print()

        prompt = input("Is this okay?(y/n/quit)").lower()
        if prompt == "y":
            break
        elif prompt == "quit":
            return

    alarms.append({"title": title, "hour": alarmHour, "minute": alarmMinute,
                   "repeating": True if repeating == "y" else False})
    return


def alarmWatch(alarms: List[Dict]):
    while True:
        now = datetime.datetime.now()
        for i in range(len(alarms)):
            if alarms[i]["hour"] == now.hour and alarms[i]["minute"] == now.minute:
                print("Ring the bell, its [" + alarms[i]["title"] + "] time")
                playsound("alarm.mp3", False)
                if not alarms[i]["repeating"]:
                    del alarms[i]
            time.sleep(1/60)
        time.sleep(1/24)


def load_alarms() -> List:
    if not os.path.isfile(".\\alarms.json"):
        return []

    with open("alarms.json", "r", encoding="utf-8") as fp:
        return json.load(fp)


def save_alarms(alarms: Dict):
    with open("alarms.json", "w", encoding="utf-8") as fp:
        json.dump(alarms, fp)
    return


def main():
    clear_screen()
    alarms = load_alarms()
    if not alarms:
        print("There is no alarm loaded. Please set an alarm...")
        createAlarm(alarms)
        clear_screen()

    print("Naz Alarm App")

    print("Starting thread for alarm(s)")
    alarm_thread = threading.Thread(
        target=alarmWatch, args=(alarms,), daemon=True)
    alarm_thread.start()
    print("Started the alarm thread")

    print()
    print()
    while 1:
        print("Press [1] to see all the alarm")
        print("Press [2] to set a new alarm")
        print()
        print("Press [0] to quit")

        while 1:
            key_pressed = getch().decode("utf-8")
            clear_screen()
            if key_pressed == "1":
                print()
                # print("!!!SHOW ALL THE ALARMS!!!")
                print(alarms)
                print()
                pressSpaceToContinue()
                break
            elif key_pressed == "2":
                print()
                createAlarm(alarms)
                print()
                pressSpaceToContinue()
                break
            elif key_pressed == "0":
                save_alarms(alarms)
                return 0


if __name__ == "__main__":
    main()
