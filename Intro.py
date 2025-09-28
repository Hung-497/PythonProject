import colorama
from art import *
from pyfiglet import Figlet
from colorama import init, Fore, Style, Back
def show_intro():
    print(Fore.RED + Style.BRIGHT,end='')
    lprint(length=90, height=1, char="*")
    f = Figlet(width=100).renderText("Survival - Flight")
    print(f)
    lprint(length=90, height=1, char="*")
    print(Style.RESET_ALL, end=' ')
