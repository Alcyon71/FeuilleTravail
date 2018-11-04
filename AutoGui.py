import pyautogui as pygui
from time import sleep

sleep(10)
print('ok')
pygui.typewrite('Hello Word!\n', interval=0.25)
sleep(1)
pygui.typewrite('Test1')

