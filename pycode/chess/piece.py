user_color = {1: "blue", 2: "red"}


# 棋子类
class piece(object):
    # 类的静态变量用于自动给棋子标记id
    user1_count = 0
    user2_count = 0

    def __init__(self, user):
        self.user = user
        self.color = user_color[user]
        self.pos = [0, 0]
        if user == 1:
            self.id = piece.user1_count
            piece.user1_count += 1
        elif user == 2:
            self.id = piece.user2_count
            piece.user2_count += 1

    # 析构函数 棋子重置后自动减少计数
    def __del__(self):
        if self.user == 1:
            piece.user1_count -= 1
        elif self.user == 2:
            piece.user2_count -= 1

    # 设置棋子位置pos
    def set_pos(self, pos):
        self.pos = pos
