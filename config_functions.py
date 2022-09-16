from libqtile.lazy import lazy
import subprocess
import os

@lazy.function
def change_keyboard(qtile, current_keyboard:str) -> None:
    if (current_keyboard == 'us'):
        current_keyboard = 'latam'
    elif (current_keyboard == 'latam'):
        current_keyboard = 'us'
    subprocess.run(["setxkbmap", current_keyboard])
