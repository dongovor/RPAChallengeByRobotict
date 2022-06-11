from tkinter import *
import config
from pynput import keyboard
import time


start_time = None
elapsed_time = None
stop_flag = False

# init form and label
tk_root = Tk()
tk_root.title("Stopwatch")
tk_root.geometry("500x100")
tk_label = Label(tk_root, text=config.MAIN_DIALOG_MESSAGE,
                 anchor="e",
                 justify=LEFT,
                 font=("Helvetica", 18))
tk_label.place(x=10, y=10)


def time_converter(sec) -> str:
    """
    Convert seconds to hours:minutes:seconds
    """
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    elapsed = f"{int(hours)}:{int(mins)}:{int(sec).__round__(2)}"
    return elapsed


def on_activate_start_pause() -> None:
    """
    Start/Pause the stopwatch when <ctrl>+<shift>+s is pressed
    """
    global start_time, elapsed_time, tk_label
    if start_time is None:
        start_time = time.time()
        tk_label.config(
                text="SuperMega Stopwatch is running",
                font=("Helvetica", 28),
                background="green")
    else:
        if elapsed_time is None:
            elapsed_time = time.time() - start_time
            tk_label.config(
                text="SuperMega Stopwatch is running",
                font=("Helvetica", 28),
                background="green")
        else:
            elapsed_time = elapsed_time + (time.time() - start_time)
            start_time = None
            tk_label.config(
                text=f"Paused. Elapsed: {time_converter(elapsed_time)}",
                font=("Helvetica", 28),
                background="green")


def on_activate_stop() -> None:
    """
    Stop the program when <ctrl>+<shift>+s is pressed
    """
    global start_time, elapsed_time, stop_flag
    if elapsed_time is None:
        tk_label.config(
            text="Please start the stopwatch first",
            font=("Helvetica", 32),
            background="red")
    else:
        tk_label.config(
            text=f"Stopped. Elapsed: {time_converter(elapsed_time)}",
            font=("Helvetica", 32),
            background="red")
        stop_flag = True
        start_time = None
        elapsed_time = None


def on_activate_quit() -> None:
    """
    Quit the program when <ctrl>+<shift>+q is pressed
    """
    global stop_flag
    stop_flag = True
    print("Quitting")
    tk_root.quit()
    quit()


hotkeys = keyboard.GlobalHotKeys({
    '<ctrl>+<shift>+a': on_activate_start_pause,
    '<ctrl>+<shift>+s': on_activate_stop,
    '<ctrl>+<shift>+q': on_activate_quit})

hotkeys.start()
tk_root.mainloop()


def main():
    while True:
        if stop_flag:
            break


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Unexpected error: {e}')
