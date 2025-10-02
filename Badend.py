from art import *
from pyfiglet import Figlet
from colorama import Fore, Style

def show_bad_end():
    print(Fore.RED + Style.BRIGHT, end='')
    lprint(length=250, height=1, char="*")
    banner = Figlet(font='ansi_shadow', width=200, justify='center').renderText(">>> Game Over! <<<")
    print(banner)
    print("Unfortunately, the clock expired and Red Death prevailed. You've lost many of lives.")
    lprint(length=250, height=1, char="*")
    print(Style.RESET_ALL, end='')
