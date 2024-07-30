from colorama import init, Fore, Back, Style
init()
from time import sleep
from wcwidth import wcwidth

def display(text: str, end="\n", fore=Fore.RESET, back=Back.RESET, prompt=Style.DIM):
    print(fore, back, end="")
    is_in_prompt = False
    char_width_in_prompt = 0
    
    def backspace_and_clear(num):
        # For each character width, print '\b \b' to clear the character
        for _ in range(num):
            print("\b \b", end="")

    for x in text:
        if x == "{":
            is_in_prompt = True
            print(prompt, end="")
            char_width_in_prompt = 0
        elif x == "}":
            backspace_and_clear(char_width_in_prompt)
            is_in_prompt = False
            print(Style.RESET_ALL, end="")
        else:
            width = wcwidth(x)
            if is_in_prompt:
                char_width_in_prompt += width
            print(x, end="", flush=True)
        sleep(0.05)
    print(Style.RESET_ALL, end=end)

display("{しんだ}死んだ{へんすう}変数で{く}繰り{かえ}返す")
display("{かぞ}数え{ごと}事が{はら}孕んだ{ねつ}熱")
display("どこに{おく}送るあてもなく")
display("{あわ}哀れな{ひと}独り{ごと}言を{しる}記している")
