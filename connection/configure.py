import os
import json
import platform

from datetime import datetime
from contextlib import contextmanager

os_type = platform.system()

@contextmanager
def find_and_make_prefs(dbfile = "chinook.db"):
    userpath = os.path.expanduser("~")
    file_path, pref_file = get_files(userpath, dbfile)
    pref_list = check_if_json_exists(file_path, pref_file)
    if pref_list != {}:
        use_existing = input("Existing preferences and history file found.\n Enter 'ignore' to ignore, or enter to use: ")
        if use_existing != "":
            pref_list = {}
    # Find a way to get this to return a list of reports and queries from running cmdloop
    yield
    report_name = "Some report name"
    query_string = "select * from *"
    write_pref_file(pref_file, pref_list, dbfile, report_name, query_string)



def get_files(userpath, dbfile):
    if os_type == "Windows":
        file_path = f"{userpath}\AppData\Local\{dbfile}\settings"
        pref_file = f"{file_path}\settings.json"
    else:
        file_path = f"{userpath}/Library/Preferences"
        pref_file = f"{file_path}/{dbfile}_config_settings.json"
    return file_path, pref_file

def check_if_json_exists(file_path, pref_file):
    if os.path.exists(file_path):
        try:
            with open(pref_file, "r") as prefs:
                try:
                    pref_list = json.load(prefs)
                except json.JSONDecodeError as err:
                    print("prefence file is empty")
                    pref_list = {}
        except FileNotFoundError:
            print("No existing user preferences found")
            pref_list = {}
    else:
        print("No existing user preferences found")
        os.makedirs(file_path)
        with open(pref_file, "w+") as prefs:
            prefs.write("")
            pref_list = {}
    return pref_list

def write_pref_file(pref_file, pref_list, dbfile, report_name, query_string):
    report_last_run = str(datetime.now())
    try:
        if pref_list["Database Location"]:
            pass
    except KeyError:
        pref_list["Database Location"] = dbfile
    with open(pref_file, "w+") as prefs:
        pref_list[report_last_run] ={"Report Name": report_name, "Query": query_string}
        prefs.write(json.dumps(pref_list))
        print(pref_list)

if __name__ == "__main__":
    find_and_make_prefs()