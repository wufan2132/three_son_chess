from tkinter import *
from chess.piece import user_color
from chess.board import user1_piece, user2_piece

text_dict = {0: "①", 1: "②", 2: "③"}


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg="white")
        self.Frame1 = Frame(master, bg="white")
        self.Frame1.pack()
        self.Frame2 = Frame(master, bg="white")
        self.Frame2.pack()
        self.enable = 0
        self.button = {}
        self.createWidgets()
        self.createinput()
        # 一些标志位与缓存单位
        self.choosing = 0
        self.uesr = None

    def createWidgets(self):
        self.button[(0, 1)] = Button(self.Frame1, text="○", height=1, width=3, bg="yellow", fg="black", bd=5,
                                     relief=FLAT,
                                     command=lambda: self.choose_step(0, 1))
        self.button[(0, 1)].grid(row=0, column=1, padx=10, pady=10)

        self.button[(0, 2)] = Button(self.Frame1, text="○", height=1, width=3, bg="yellow", fg="black", bd=5,
                                     relief=FLAT, command=lambda: self.choose_step(0, 2))
        self.button[(0, 2)].grid(row=0, column=2, padx=10, pady=10)

        self.button[(0, 0)] = Button(self.Frame1, text="○", height=1, width=3, bg="yellow", fg="black", bd=5,
                                     relief=FLAT,
                                     command=lambda: self.choose_step(0, 0))
        self.button[(0, 0)].grid(row=0, column=0, padx=10, pady=10)

        self.button[(1, 0)] = Button(self.Frame1, text="○", height=1, width=3, bg="yellow", fg="black", bd=5,
                                     relief=FLAT,
                                     command=lambda: self.choose_step(1, 0))
        self.button[(1, 0)].grid(row=1, column=0, padx=10, pady=10)

        self.button[(1, 1)] = Button(self.Frame1, text="○", height=1, width=3, bg="yellow", fg="black", bd=5,
                                     relief=FLAT,
                                     command=lambda: self.choose_step(1, 1))
        self.button[(1, 1)].grid(row=1, column=1, padx=10, pady=10)
        self.button[(1, 2)] = Button(self.Frame1, text="○", height=1, width=3, bg="yellow", fg="black", bd=5,
                                     relief=FLAT,
                                     command=lambda: self.choose_step(1, 2))
        self.button[(1, 2)].grid(row=1, column=2, padx=10, pady=10)
        self.button[(2, 0)] = Button(self.Frame1, text="○", height=1, width=3, bg="yellow", fg="black", bd=5,
                                     relief=FLAT,
                                     command=lambda: self.choose_step(2, 0))
        self.button[(2, 0)].grid(row=2, column=0, padx=10, pady=10)
        self.button[(2, 1)] = Button(self.Frame1, text="○", height=1, width=3, bg="yellow", fg="black", bd=5,
                                     relief=FLAT,
                                     command=lambda: self.choose_step(2, 1))
        self.button[(2, 1)].grid(row=2, column=1, padx=10, pady=10)
        self.button[(2, 2)] = Button(self.Frame1, text="○", height=1, width=3, bg="yellow", fg="black", bd=5,
                                     relief=FLAT,
                                     command=lambda: self.choose_step(2, 2))
        self.button[(2, 2)].grid(row=2, column=2, padx=10, pady=10)

    def createinput(self):
        self.Input = Entry(self.Frame2)
        self.Input.pack(side=LEFT)
        self.Input.text = ""
        self.okbutton = Button(self.Frame2, text="OK", height=1, width=3)
        self.okbutton.pack(side=LEFT)

    def show(self, board):
        for pos in board.pos:
            if board.pos[pos] == None:
                self.button[pos].config(text="○", bg="white")
            else:
                color = board.pos[pos].color
                id = board.pos[pos].id
                self.button[pos].config(text=text_dict[id], bg=color)

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

    def choose_step(self, x, y):
        piece_id = 0
        if self.uesr == 1:
            user_piece = user1_piece
        else:
            user_piece = user2_piece
        for piece in user_piece:
            if piece.pos == [x, y]:
                piece_id = piece.id
                break

        if len(self.Input.text) <= 4 and self.Input.text != "":
            self.Input.text += self.get_action_name([x, y], int(self.Input.text[0])-1)
        else:
            self.Input.text = str(piece_id+1) + ": "
        self.Input.delete(0, END)
        self.Input.insert(0, self.Input.text)


    def get_action_name(self, pos, piece_id):
        if self.uesr == 1:
            user_piece = user1_piece
        else:
            user_piece = user2_piece
        pos_ = user_piece[piece_id].pos
        if pos == [1, 1]:
            return "center"
        elif pos[0] - pos_[0] == -1 and pos[1] == pos_[1]:
            return "up"
        elif pos[0] - pos_[0] == 1 and pos[1] == pos_[1]:
            return "down"
        elif pos[0] - pos_[0] == 0 and pos[1] == pos_[1] - 1:
            return "left"
        elif pos[0] - pos_[0] == 0 and pos[1] == pos_[1] + 1:
            return "right"
        elif pos[0] - pos_[0] == -1 and pos[1] == pos_[1] - 1:
            return "up_left"
        elif pos[0] - pos_[0] == 1 and pos[1] == pos_[1] - 1:
            return "down_left"
        elif pos[0] - pos_[0] == -1 and pos[1] == pos_[1] + 1:
            return "up_right"
        elif pos[0] - pos_[0] == 1 and pos[1] == pos_[1] + 1:
            return "down_right"
        else:
            return "unknow"
