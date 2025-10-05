from art import *
from pyfiglet import Figlet
from colorama import Fore, Style

def show_good_end():
    print(Fore.YELLOW + Style.BRIGHT, end='')
    lprint(length=250, height=1, char="*")
    banner = Figlet(font='ansi_shadow', width=200, justify='center').renderText(">>> Game Win! <<<")
    print(banner)
    print(f'You finally piece together the entire message.\nThe last computer flickers as the decoded text scrolls across the screen, line by line.\nIt’s all so clear now—your mistake, the collapse, the reason everything has been fading away.\nMemories you’d buried under years of silence come rushing back like a tidal wave.\nAnd then… peace.\nThe countdown hits zero, but the world doesn’t explode. It just… quiets. You walk outside the terminal, past empty halls and forgotten signs, until you find the same bench where it all began. \nThe sky is painted in soft evening light. You lie down, not as a savior, but as someone who finally understands. Some battles can’t be won, and accepting that might be the only real victory left.')
    lprint(length=250, height=1, char="*")
    print(Style.RESET_ALL, end='')
