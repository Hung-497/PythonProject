from art import *
from pyfiglet import Figlet
from colorama import init, Fore, Style

def show_intro():
    init(autoreset=True)
    print(Fore.RED + Style.BRIGHT, end='')
    lprint(length=180, height=1, char="*")
    banner = Figlet(font='ansi_shadow', width=200).renderText("Survival - Flight \nBy : Group - 1")
    print(banner)
    lprint(length=180, height=1, char="*")
    print(Style.RESET_ALL, end='')
