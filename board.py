from PIL import Image, ImageDraw, ImageFont
import random, time
import clipboard
import win32.win32clipboard as win32clipboard
from io import StringIO, BytesIO
from threading import Lock
imagLock = Lock()

called_no = []
last_called = []

def draw_board(called_list, last_called):
    imagLock.acquire()
    img = Image.new('RGB', (5000, 4500), color='white')
    draw = ImageDraw.Draw(img)
    for no in range(1,91):
        if len(called_list) and no == called_list[-1]:
            font_color = "black"
            block_color = "cyan"
        elif no in called_list:
            font_color = "black"
            block_color = "green"
        else:
            font_color = "white"
            block_color = "grey"
        draw_no(draw, no, font_color=font_color, bkg_color=block_color)
    img.save("board.png")
    img.close()
    imagLock.release()

def copy_board_to_clipboard():
    imagLock.acquire()
    img = Image.open('board.png')
    output = BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)
    img.close()
    imagLock.release()

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def draw_no(draw, no, font_color, bkg_color):
    row = int((no-1)/10)
    col = (no-1 - (row*10)) % 10
    x = col * 500
    y = row * 500
    shape = [(x, y), (x + 490, y+490)]
    fnt = ImageFont.truetype("arial", 200)
    draw.rectangle(shape, fill =bkg_color, outline ="black")
    draw.text((x+100,y+100), str(no), font=fnt, fill=font_color)



