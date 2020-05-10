from tkinter import *
from PIL import Image, ImageTk
from board import draw_board
from random import sample, shuffle, choice
import time
from threading import Thread
from WhatsApp import WhatsApp
import os
import sys
try:
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH  = '.'

class App(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.root = master
        self.board = Canvas(self, bd=0, highlightthickness=0)
        self.board.configure(width=500, height=500)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.wp_group_name = ""
        self.start_button = Button(master, text="Start", command=self.start)
        self.pause_button = Button(master, text="Pause", command=self.pause)
        self.send_board_button = Button(master, text="Send Board", command=self.send_board)
        self.resume_button = Button(master, text="Resume", command=self.resume)
        self.fast_button = Button(master, text="Fast", command=self.fast)
        self.slow_button = Button(master, text="Slow", command=self.slow)
        self.next_number_in = StringVar()
        self.label_next_number_delay = Label(master, textvariable=self.next_number_in)
        self.called_no = []
        self.last_called_no = []
        self.un_called = sample(range(1,91), 90)
        self.speed=8
        self.delay = self.speed
        self.next_number_in.set(self.speed)
        self.button_next_number = Button(master, text="Next Number", command=self.next_number)

        self.min_speed = 2
        self.max_speed = 30
        self.paused = False
        self.num_map = None
        self.get_number_map()
        self.initialize()

    def next_number(self):
        self.delay = 0


    def slow(self):
        if (self.speed + 1) > self.max_speed:
            self.speed = self.max_speed
        else:
            self.speed = self.speed + 1

    def fast(self):
        if (self.speed - 1) < self.min_speed:
            self.speed = self.min_speed
        else:
            self.speed = self.speed - 1

    def initialize(self):
        canvas1 = Canvas(self.root, width=400, height=300)
        canvas1.pack()
        entry1 = Entry(self.root)
        canvas1.create_window(200, 140, window=entry1)
        def set_group_name():
            self.wp_group_name = entry1.get()
            canvas1.forget()
            self.draw_canvas()
            self.start_button.pack()
            self.wp = WhatsApp(self.wp_group_name)
            self.wp.send_text("Lets Begin...")
        button1 = Button(text='Enter the group name', command=set_group_name)
        canvas1.create_window(200, 180, window=button1)

    def get_number_map(self):
        path = os.path.join(BASE_PATH, 'numbers.txt')
        with open(path) as f:
            data = f.read().split("\n")
        num_map = {}
        for ln in data:
            ln = ln.split("\t")
            num = int(ln[0])
            msg = ln[1:]
            num_map[num] = msg
        self.num_map = num_map

    def send_board(self):
        self.wp.send_board()

    def pause(self):
        self.paused = True
        if len(self.called_no)>3:
            self.wp.send_text("Last three no.. %s" %str(self.called_no[-3:]))
        self.send_board()
        self.pause_button.forget()
        self.resume_button.pack()

    def resume(self):
        self.wp.send_text("Next Number....")
        self.paused = False
        self.pause_button.pack()
        self.resume_button.forget()
        self.send_board_button.forget()

    def draw_canvas(self):
        draw_board(self.called_no, self.last_called_no)
        self.board.delete()
        self.board.configure(width=500, height=500)
        self.original = Image.open('board.png')
        self.original = self.original.resize((500,500))
        self.image = ImageTk.PhotoImage(self.original)
        self.board.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")
        self.board.grid(row=0, sticky=W + E + N + S)
        self.pack(fill=BOTH, expand=1)


    def start(self):
        def fun():
            while True:
                if not self.paused:
                    shuffle(self.un_called)
                    next_no = self.un_called.pop()
                    self.called_no.append(next_no)
                    self.draw_canvas()
                    msg = choice(self.num_map[next_no])
                    self.wp.send_text("%d -- %s" %(next_no, msg))
                    while self.delay > 0:
                        print(self.delay)
                        self.next_number_in.set(int(self.delay))
                        self.delay -= 0.1
                        time.sleep(0.1)
                    else:
                        self.delay = self.speed
                else:
                    time.sleep(5)
        Thread(target=fun).start()
        self.pause_button.pack(side=LEFT, padx=10)
        self.send_board_button.pack(side=LEFT, padx=10)
        self.button_next_number.pack(side=LEFT, padx=20)
        self.fast_button.pack(side=RIGHT, padx=5)
        self.label_next_number_delay.pack(side=RIGHT, padx=5)
        self.slow_button.pack(side=RIGHT, padx=5)
        self.start_button.forget()



root = Tk()
app = App(root)
app.mainloop()
root.destroy()