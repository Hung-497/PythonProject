from art import *
from pyfiglet import Figlet
from colorama import Fore, Style

def show_good_end():
    print(Fore.YELLOW + Style.BRIGHT, end='')
    lprint(length=250, height=1, char="*")
    banner = Figlet(font='ansi_shadow', width=200, justify='center').renderText(">>> Game Win! <<<")
    print(banner)
    print(f'You rescued millions and safeguarded the world. We’re forever grateful, our hero.')
    lprint(length=250, height=1, char="*")
    print(Style.RESET_ALL, end='')
