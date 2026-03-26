import os
import time
import re
try:
    import msvcrt  # Windows-only, used for skippable typewriter
except ImportError:  # non-Windows fallback
    msvcrt = None

def safe_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nInput interrupted. Exiting game.")
        exit()

def red(text):
    return f"\033[31m{text}\033[0m"

def green(text):
    return f"\033[32m{text}\033[0m"

def yellow(text):
    return f"\033[33m{text}\033[0m"

def brown(text):
    # Use ANSI yellow as a readable "brown" approximation in most terminals
    return f"\033[33m{text}\033[0m"

def bold(text):
    return f"\033[1m{text}\033[0m"

def cls():
    return os.system('cls' if os.name == 'nt' else 'clear')

_ANSI_RESET = "\033[0m"
_COLOR_CODES = {
    "red": "31",
    "green": "32",
    "yellow": "33",
    "brown": "33",
}

_ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")

def type_out(text, delay=0.015, color: str = None, skippable: bool = True):
    """Print text like a typewriter, with optional color and skip-on-keypress.
    - color: one of 'red','green','yellow','brown'
    - skippable: if True on Windows, pressing any key will print the rest instantly
    """
    plain = _ANSI_PATTERN.sub("", str(text))
    prefix = f"\033[{_COLOR_CODES.get(color, '')}m" if color in _COLOR_CODES else ""
    suffix = _ANSI_RESET if prefix else ""
    if prefix:
        print(prefix, end="", flush=True)

    i = 0
    n = len(plain)
    while i < n:
        # If skippable and on Windows, allow keypress to dump the rest of the line
        if skippable and msvcrt is not None and msvcrt.kbhit():
            # Clear all buffered keypresses so they don't leak into next input
            try:
                while msvcrt.kbhit():
                    msvcrt.getch()
            except Exception:
                pass
            # Print remaining text instantly
            print(plain[i:], end="", flush=True)
            i = n
            break

        print(plain[i], end="", flush=True)
        time.sleep(delay)
        i += 1

    if suffix:
        print(suffix, end="")
    print()

