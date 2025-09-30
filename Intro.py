from art import *
from pyfiglet import Figlet
from colorama import init, Fore, Style, Back
def show_intro():
    print(Fore.RED + Style.BRIGHT,end='')
    lprint(length=180, height=1, char="*")
    f = Figlet(font='ansi_shadow', width=200).renderText("Survival - Flight \nBy : Group - 1")
    print(f)
    lprint(length=180, height=1, char="*")
    print(Style.RESET_ALL, end=' ')
show_intro()


