from tkinter import *
from chess.piece import user_color

text_dict = {0: "①", 1: "②", 2: "③"}


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg="white")
        self.Frame1

        self.pack()
        self.enable = 0
        self.button = {}
        self.createWidgets()
        self.createinput()
        #
        self.choosing = 0
        self.uesr = None

    def createWidgets(self):
        for i in range(3):
            for j in range(3):
                self.button[(i, j)] = Button(self, text="○", height=1, width=3,
                                             bg="yellow", fg="black",
                                             bd=5, relief=FLAT)
                self.button[(i, j)].grid(row=i, column=j, padx=10, pady=10)

    def createinput(self):
        self.okbutton = Button(self, text="OK")
        self.okbutton.pack()
        self.Input = Entry(self)
        self.Input.pack()

    def show(self, board):
        for pos in board.pos:
            if board.pos[pos] == None:
                self.button[pos].config(text="○", bg="white", command=None)
            else:
                color = board.pos[pos].color
                id = board.pos[pos].id
                self.button[pos].config(text=text_dict[id], bg=color)
                if self.enable == 1 and board.pos[pos].user == self.uesr:
                    self.button[pos].config(command=self.choose_step)
                else:
                    self.button[pos].config(command=None)

    def show_winner(self, board, winner):
        for pos in board.pos:
            if board.pos[pos] == None or board.pos[pos].user != winner:
                self.button[pos].config(text="○", bg="white")
            else:
                color = board.pos[pos].color
                id = board.pos[pos].id
                self.button[pos].config(text=text_dict[id], bg=color)

    def enable_control(self, user=2):
        self.enable = 1
        self.uesr = user

    def choose_step(self):
        pass



