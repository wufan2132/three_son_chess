from chess.piece import piece
from chess.operate import operate_dict, operate_reverse

user1_piece = []
user2_piece = []
action_array = ["up", "down", "left", "right", "center", "up_left", "down_left", "up_right", "down_right"]


# 棋盘类
class board(object):
    # 初始化棋盘
    def __init__(self, size=3):
        self.size = size  # 实际上只支持3*3
        self.pos = {}  # 用dict存储对应位置的棋子
        for i in range(self.size):
            for j in range(self.size):
                self.pos[(i, j)] = None
        self.reset()

    # -----------------------public----------------------------------------------#
    #  重新放子上去
    def reset(self):
        # 清空棋盘
        for i in range(self.size):
            for j in range(self.size):
                self.pos[(i, j)] = None
        # 清空双方棋子
        user1_piece.clear()
        user2_piece.clear()
        # 初始化棋子
        for i in range(3):
            p = piece(user=1)
            self.__put_piece(p, [0, i])
            user1_piece.append(p)
        for i in range(3):
            p = piece(user=2)
            self.__put_piece(p, [2, i])
            user2_piece.append(p)

    # 获得某个棋子的可行操作，av = available
    def get_feasible_operate(self, piece):
        Feasible_array = []
        # up
        pos = piece.pos.copy()
        pos[0] -= 1
        if pos[0] >= 0 and pos[0] < self.size and self.pos[tuple(pos)] == None:
            Feasible_array.append("up")
        # down
        pos = piece.pos.copy()
        pos[0] += 1
        if pos[0] >= 0 and pos[0] < self.size and self.pos[tuple(pos)] == None:
            Feasible_array.append("down")
        # right
        pos = piece.pos.copy()
        pos[1] += 1
        if pos[1] >= 0 and pos[1] < self.size and self.pos[tuple(pos)] == None:
            Feasible_array.append("right")
        # left
        pos = piece.pos.copy()
        pos[1] -= 1
        if pos[1] >= 0 and pos[1] < self.size and self.pos[tuple(pos)] == None:
            Feasible_array.append("left")
        # center
        pos = piece.pos
        if pos != [1, 1] and self.pos[(1, 1)] == None:
            Feasible_array.append("center")
        # else
        pos = piece.pos
        if pos == [1, 1]:
            if self.pos[(2, 0)] == None:
                Feasible_array.append("down_left")
            if self.pos[(2, 2)] == None:
                Feasible_array.append("down_right")
            if self.pos[(0, 0)] == None:
                Feasible_array.append("up_left")
            if self.pos[(0, 2)] == None:
                Feasible_array.append("up_right")
        return Feasible_array

    # 获得某个使用者的可行操作，放在list里
    def get_Feasible_operate_array(self, user):
        if (user == 1):
            vector = []
            user_piece = user1_piece.copy()
            user_piece = sorted(user_piece, key=lambda p: 3 * p.pos[0] + p.pos[1])
            for piece in user_piece:
                Feasible_array = self.get_feasible_operate(piece)
                vector += [x in Feasible_array for x in action_array]
            return vector
        elif (user == 2):
            vector = []
            user_piece = user2_piece.copy()
            user_piece = sorted(user_piece, key=lambda p: 3 * (2 - p.pos[0]) + 2 - p.pos[1])
            for piece in user_piece:
                Feasible_array = self.get_feasible_operate(piece)
                Feasible_array = [operate_reverse[F] for F in Feasible_array]
                vector += [x in Feasible_array for x in action_array]
            return vector

    # 判断是否存在可行操作
    def is_operate_Feasible(self, piece, operate):
        Feasible_array = self.get_feasible_operate(piece)
        if operate in Feasible_array:
            return 1
        else:
            return 0

    # 根据操作移动固定棋子
    def move_piece(self, piece, operate):
        Feasible_array = self.get_feasible_operate(piece)
        if operate in Feasible_array:
            self.pos[tuple(piece.pos)] = None
            operate_dict[operate](piece.pos)
            self.pos[tuple(piece.pos)] = piece
            return 1
        else:
            print("error: operate is wrong!")
            print("piece.color:", piece.color)
            print("operate:", operate)
            return 0

    # 判断是否有人获胜，获胜条件：3个棋子斜着连成一条线，或者对方无棋可走
    def is_Win(self):
        Feasible_array = []
        for piece in user1_piece:
            Feasible_array += self.get_feasible_operate(piece)
        if Feasible_array == []:
            return 2
        Feasible_array = []
        for piece in user2_piece:
            Feasible_array += self.get_feasible_operate(piece)
        if Feasible_array == []:
            return 1
        if self.pos[(1, 1)] != None and self.pos[(1, 1)].user == 1:
            if (self.pos[(0, 0)] != None and self.pos[(2, 2)] != None and self.pos[(0, 0)].user == 1
                and self.pos[(2, 2)].user == 1) \
                    or (self.pos[(0, 2)] != None and self.pos[(2, 0)] != None and self.pos[(0, 2)].user == 1 and
                        self.pos[(2, 0)].user == 1):
                return 1
            else:
                return None
        elif self.pos[(1, 1)] != None and self.pos[(1, 1)].user == 2:
            if (self.pos[(0, 0)] != None and self.pos[(2, 2)] != None and self.pos[(0, 0)].user == 2 and
                self.pos[(2, 2)].user == 2) \
                    or (self.pos[(0, 2)] != None and self.pos[(2, 0)] != None and self.pos[(0, 2)].user == 2 and
                        self.pos[(2, 0)].user == 2):
                return 2
            else:
                return None
        return None

    # -----------------------private----------------------------------------------#
    #  移动某个棋子到指定位置
    def __put_piece(self, piece, p):
        self.pos[tuple(p)] = piece
        piece.pos = p

