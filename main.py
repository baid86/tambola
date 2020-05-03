from tkinter import *
from PIL import Image, ImageTk
from board import draw_board
from random import sample, shuffle, choice
import time
from threading import Thread
from WhatsApp import WhatsApp
class App(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.board = Canvas(self, bd=0, highlightthickness=0)
        self.board.configure(width=500, height=500)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.start_button = Button(master, text="Start", command=self.start)
        self.pause_button = Button(master, text="Pause", command=self.pause)
        self.send_board_button = Button(master, text="Send Board", command=self.send_board)
        self.resume_button = Button(master, text="Resume", command=self.resume)

        self.start_button.pack()
        self.called_no = []
        self.last_called_no = []
        self.un_called = sample(range(1,91), 90)
        self.time_interval=15
        self.paused = False
        self.num_map = None
        self.get_number_map()



    def get_number_map(self):
        with open('numbers.txt') as f:
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
        self.wp = WhatsApp('Gharelu housie group')
        self.wp.send_text("Lets Begin...")
        def fun():
            while True:
                if not self.paused:
                    shuffle(self.un_called)
                    next_no = self.un_called.pop()
                    self.called_no.append(next_no)
                    self.draw_canvas()
                    msg = choice(self.num_map[next_no])
                    self.wp.send_text("%d -- %s" %(next_no, msg))
                    time.sleep(self.time_interval)
                else:
                    time.sleep(5)
        Thread(target=fun).start()
        time.sleep(5)
        self.pause_button.pack()
        self.send_board_button.pack()
        self.start_button.forget()


root = Tk()
app = App(root)
app.mainloop()
root.destroy()