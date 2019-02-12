import sys
import pyautogui

def pyautogui_test():
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print (positionStr,end="")
            print ('\b' * (len(positionStr) + 2),end="")
            sys.stdout.flush()
    except KeyboardInterrupt:
        print ('\n')


if (__name__ == "__main__"):
    pyautogui_test()