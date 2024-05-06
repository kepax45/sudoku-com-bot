import base64

import cv2
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import numpy as np
import easyocr
import math
from sudoku_solver import *
import copy
import chromedriver_autoinstaller


def custom_find(element, by, string):
    res = element.find_element(by, string)
    while res is None:
        res = element.find_element(by, string)
    return res
def custom_click(element, delay):
    element.click()
    time.sleep(delay)
def custom_get(element, link):
    element.get(link)
    time.sleep(2)

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.page_load_strategy = 'eager'

reader = easyocr.Reader(['en'], gpu=False)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
custom_get(driver, "https://sudoku.com/extreme")
note = custom_find(driver, By.CLASS_NAME, "game-tip")
game_div = custom_find(driver, By.ID, 'game')
canvas = custom_find(game_div, By.TAG_NAME, 'canvas')
custom_click(canvas, 1)
base64text = canvas.screenshot_as_base64
image_bytes = base64.b64decode(base64text)
image_np = np.frombuffer(image_bytes, dtype=np.uint8)
image_cv = cv2.imdecode(image_np, cv2.IMREAD_GRAYSCALE)
(thresh, image_cv) = cv2.threshold(image_cv, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
width, height = image_cv.shape
cell_dimensions = math.ceil(width/9)
cv2.imshow('table', image_cv)
grid = [[0 for i in range(9)] for i in range(9)]
for i in range(9):
    for j in range(9):
            image_piece = image_cv[i*cell_dimensions:(i+1)*cell_dimensions, j*cell_dimensions:(j+1)*cell_dimensions]
            scale_factor = 2
            upscaled = cv2.resize(image_piece, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
            blur = cv2.blur(upscaled, (5, 5))
            results = reader.readtext(blur, text_threshold=0.3)
            if(results!=[]):
                digit = results[0][1]
                grid[i][j] = int(digit)

for row in grid:
        print(row)
unsolved_grid = copy.deepcopy(grid)
solve(grid)
print()
for row in grid:
        print(row)
game_div = custom_find(driver, By.ID, 'game')
time.sleep(2)
canvas = custom_find(game_div, By.TAG_NAME, 'canvas')
time.sleep(2)


actions = ActionChains(driver)

time.sleep(2)

canvas_x = canvas.location['x']
canvas_y = canvas.location['y']
cell_dimensions = math.ceil(canvas.size['width']/9)
actions.move_by_offset(canvas_x, canvas_y).click().perform()
for i in range(9):
    for j in range(9):
        if grid[i][j] != unsolved_grid[i][j]:
            actions.send_keys(str(grid[i][j])).perform()
        actions.move_by_offset(cell_dimensions, 0).click().perform()
    actions.move_by_offset(-9*cell_dimensions, cell_dimensions).click().perform()

cv2.waitKey(0)
cv2.destroyAllWindows()
driver.close()

