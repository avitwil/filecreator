import os
import subprocess
import time
from time import sleep

import keyboard


def clear_screen():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Other systems (Linux, macOS)
    else:
        os.system('clear')

def get_valid_file_name()->str:
    try:
        file_name = input("enter file name: ")
        if len(file_name) >= 1:
            check = True
        else:
            check = False
        for i in file_name:
            if not(i.isalnum() or i == "_"):
                check = False
        if check:
            return file_name
        else:
            return get_valid_file_name()
    except Exception as e:
        print(f"somthing went wrong \n {e}")


class CostumeTextFile:
    try:

        def __init__(self, file_name: str, file_path: str, file_type: str):
            match file_type:
                case "python":
                    self.type = "python"
                    self.file_name = f"{file_name}.py"
                case "bash":
                    self.type = "bash"
                    self.file_name = f"{file_name}.sh"
                case "text":
                    self.type = "text"
                    self.file_name = f"{file_name}.txt"
                case _:
                    self.type = "NoneType"
                    self.file_name = file_name
            if file_path == "pwd":
                self.file_path = os.getcwd()
            else:
                self.file_path = file_path
            self.full_path = os.path.join(self.file_path, self.file_name)
            self.file = None
            # Note: the shebang is written and the file is made executable
            # in create_file(), once self.file actually points to an open
            # file handle. Doing it here was a no-op, since self.file is
            # always None at construction time.

        def __repr__(self):
            return f"File Name: {self.file_name}\nFile Type:{self.type}\nLocation:{self.file_path}"

        def create_file(self,replace_if_exist: str):
            is_new_file = False
            if os.path.exists(self.full_path):
                print(f"file {self.file_name} already exist at \n {self.file_path}")
                match replace_if_exist:
                    case "y":
                        os.remove(self.full_path)
                        self.file = open(self.full_path, "x+t")
                        is_new_file = True
                    case "e":
                        self.file = open(self.full_path, "r+t")
                    case _:
                        self.file = None
            else:
                self.file = open(self.full_path, "x+t")
                is_new_file = True

            if is_new_file:
                if self.type == "python":
                    self.write_new_line("#!/bin/python\n")
                elif self.type == "bash":
                    self.write_new_line("#!/bin/bash\n")
                if self.type in ("python", "bash") and os.name != 'nt':
                    os.chmod(self.full_path, os.stat(self.full_path).st_mode | 0o111)

            return self.file

        def delete_file(self)->bool:
            if not self.file is None:
                self.close_file()
                os.remove(self.full_path)
                return True
            else:
                return False

        def close_file(self):
            if not self.file is None:
                self.file.close()

        def print_line_by_line(self):
            self.file.seek(0)
            for i in self.file.readlines():
                print(i)
                time.sleep(1)

        def write_new_line(self,text: str):
            if not self.file is None:
                self.file.write(f"{text}\n")

        def add_new_file_to_list(self):
            try:
                list_file = open("file_list.txt", "a+t")
                new_line = f"{self.file_name}-space-{self.file_path}-space-{self.type} \n"
                list_file.write(new_line)

            except Exception as e:
                print(f"somthing went wrong \n {e}")
            finally:
                try:
                    list_file.close()
                except Exception as e:
                    print(f"somthing went wrong \n {e}")

        def create_command_to_file(self,command_name: str):
            try:
                command_list_file = open("command_list.txt", "r+t")
                command_list = []
                for i in command_list_file.readlines():
                    temp_list = i.split("-space-")
                    command_list.append(CostumeCommand(temp_list[0], CostumeTextFile(temp_list[1], temp_list[2], temp_list[3])))
                for i in command_list:
                    if i.name == command_name:
                        print(f"command \"{command_name}\" already exist ")
                        break
                else:
                    new_command = CostumeCommand(command_name,self)
                    new_command.add_to_command_list()
            except Exception as e:
                print(f"somthing went wrong \n {e}")
            finally:
                try:
                    command_list_file.close()
                except Exception as e:
                    print(f"somthing went wrong \n {e}")

    except Exception as e:
        print(f"somthing went wrong \n {e}")

class CostumeCommand:
    try:
        def __init__(self,command_name: str,linked_script_file: CostumeTextFile):
            self.name = command_name
            self.script_file = linked_script_file

        def __repr__(self):
            return f"Name:{self.name}\nFile:{self.script_file.full_path}\nType:{self.script_file.type}"

        def run_command(self):
            if self.script_file.type in ["python","bash"]:
                if not os.name == 'nt' and self.script_file.file is not None:
                    os.system(self.script_file.full_path)

        def add_to_command_list(self):
            try:
                command_list_file = open("command_list.txt","a+t")
                command_list_file.write(f"{self.name}-space-{self.script_file.file_name}-space-{self.script_file.file_path}-space-{self.script_file.type} \n")
            except Exception as e:
                print(f"somthing went wrong \n {e}")
            finally:
                try:
                    command_list_file.close()
                except Exception as e:
                    print(f"somthing went wrong \n {e}")



    except Exception as e:
        print(f"somthing went wrong \n {e}")

def create_new_file():
    file_name = get_valid_file_name()
    file_path = input("enter file path(type \"pwd\" for current path): ")
    file_type = input("enter file type\n\"python\" for python script\n\"bash\" for bash script\n\"text\" for text file\nleave empty for NoneType file\ntype here:  ")
    new_file = CostumeTextFile(file_name, file_path, file_type)
    if os.path.exists(new_file.full_path):
        user_choice = input("type \"y\" to replace it or \"e\" to use it: ").lower()
    else:
        user_choice = ""
    new_file.create_file(user_choice)
    new_file.add_new_file_to_list()
    new_file.create_command_to_file(input("enter  command name: "))
    new_file.close_file()
    if os.name == 'posix':
        subprocess.run(["nano", new_file.full_path])

def show_file_list():
    try:
        list_file = open("file_list.txt", "r+t")
        for i in list_file.readlines():
            temp_list = i.split("-space-")
            print(f"------\nfile name:  {temp_list[0]}\nfile path:  {temp_list[1]}\nfile type:  {temp_list[2]}\n------")

    except Exception as e:
        print(f"somthing went wrong \n {e}")
    finally:
        try:
            list_file.close()
        except Exception as e:
            print(f"somthing went wrong \n {e}")

def show_command_list():
    try:
        command_list_file = open("command_list.txt","r+t")
        command_list =[]
        for i in command_list_file.readlines():
            temp_list = i.split("-space-")
            command_list.append(CostumeCommand(temp_list[0],CostumeTextFile(temp_list[1],temp_list[2],temp_list[3])))
            print(f"------\ncommand name:  {temp_list[0]}\nfile name:  {temp_list[1]}\nfile path:  {temp_list[2]}\nfile type:  {temp_list[3]}------")
        user_choice = input("type command to run: ")
        for i in command_list:
            if i.name == user_choice:
                i.run_command()
                break
        else:
            print(f"command '{user_choice}' not found ")

    except Exception as e:
        print(f"somthing went wrong \n {e}")
    finally:
        try:
            command_list_file.close()
        except Exception as e:
            print(f"somthing went wrong \n {e}")





def run_keyboard_menu():
    try:
        y = True
        while y:
            print("""----Welcome to my advanced File creator---
            choos your option
            1. create new file 
            2. see file list
            3. see command list
            
            you can press 'esc' to exit""")
            x = keyboard.read_key()
            match x:
                case 'esc':
                    print("Thank you for using avi twil's program")
                    exit()
                case "1":
                    y = False
                    keyboard.press('backspace')
                    keyboard.release('backspace')
                    sleep(1)
                    clear_screen()
                    create_new_file()
                case "2":
                    y = False
                    keyboard.press('backspace')
                    keyboard.release('backspace')
                    sleep(1)
                    clear_screen()
                    show_file_list()
                case "3":
                    y = False
                    keyboard.press('backspace')
                    keyboard.release('backspace')
                    sleep(1)
                    clear_screen()
                    show_command_list()
    except:
        pass








