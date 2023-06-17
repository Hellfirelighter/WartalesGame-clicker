import cv2
import numpy as np
import pyautogui
from time import sleep
import tkinter
from tkinter import *
from tkinter import ttk
import threading


def find_green_circle(image):
    # Конвертуємо зображення в HSV-простір кольорів
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Визначаємо діапазон кольорів для зеленого
    lower_green = np.array([52, 127, 165])
    upper_green = np.array([93, 205, 255])

    # Створюємо маску для зелених пікселів
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Виконуємо виявлення контурів на основі маски
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if 7000 > area > 4000:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            return center, radius

    return None, None


def mining_clicker_worker():
    while cb_checked_int_var.get() == 1:
        screenshot = pyautogui.screenshot()
        image = np.array(screenshot)

        center, radius = find_green_circle(image)

        if center is not None and radius is not None:
            pyautogui.moveTo(center[0], center[1], _pause=False)
            pyautogui.click()
            sleep(0.05)


def mining_clicker():
    t = threading.Thread(target=mining_clicker_worker, )
    if cb_checked_int_var.get() == 1 and not t.is_alive():
        t.start()


app = Tk()
app.eval('tk::PlaceWindow . center')
app.title('Clicker')
app.geometry('200x50')
app.resizable(0, 0)

cb_checked_int_var = tkinter.IntVar()
cb_mine_clicker = tkinter.Checkbutton(app,
                                      text='Mining/Chopping clicker',
                                      variable=cb_checked_int_var,
                                      onvalue=1,
                                      offvalue=0,
                                      command=mining_clicker)
cb_mine_clicker.pack(pady='10')

app.mainloop()
