from chess.GUI import Application
from chess.board import board
from chess.piece import piece
import numpy as np
import tkinter
from chess.board import user1_piece, user2_piece, action_array
from chess.operate import operate_reverse
from queue import Queue
import time


# Board = board()
# app = Application()
#
# app.show(Board)
# # 主消息循环:
# app.mainloop()


class chess_env(object):
    def __init__(self):
        self.board = board()
        # 多线程
        self.app = Application()
        # 动作空间
        self.action_space = ["up", "down", "left", "right", "center", "up_left", "down_left", "up_right", "down_right"]
        # 统计信息
        self.win1_times = 0
        self.iter_times = 0
        self.queue = Queue()
        # 标志位与缓存
        self.isyourchance = 0
        self.action_message = []

    # 环境reset
    def reset(self):
        self.board.reset()
        return self.get_obs1(), self.get_obs1(), self.get_obs2()

    # 允许人为手动控制，用于人机互搏
    def enable_control(self, user=2):
        self.app.enable_control(user)
        self.app.okbutton.config(command=self.submit)  # 将确认按钮与提交函数绑定在一起

    # 提交函数
    def submit(self):
        # 分析输出操作文本框的数据，获得人为的操作
        self.action_message = self.app.Input.text.split(": ")
        self.action_message[0] = int(self.action_message[0]) - 1
        self.action_message = [self.app.uesr] + self.action_message
        if self.app.uesr == 1:
            user_piece = user1_piece
        else:
            user_piece = user2_piece
        # 判断提交的操作是否可行
        if self.board.is_operate_Feasible(user_piece[int(self.action_message[1])], self.action_message[2]) == 1:
            self.isyourchance = 0  # 可行的话就将标志位置一
        else:  # 不可行的话清空操作文本框数据
            self.app.Input.text = ""
            self.app.Input.delete(0, tkinter.END)

    # 等待人工操作，先将标志位置一，然后不断查询isyourchance标志位，等待提交函数成功执行
    def wait_for_user(self):
        self.isyourchance = 1
        while self.isyourchance == 1:
            time.sleep(0.5)
        return self.action_message

    # 根据动作，环境做出相应的交互反应
    def step(self, action_message):
        user, piece_id, action = self.__analysis_action(action_message)
        if user == 1:
            aim_piece = user1_piece[piece_id]
        else:
            aim_piece = user2_piece[piece_id]
        self.board.move_piece(aim_piece, action)
        #
        winner = self.board.is_Win()
        # 读取环境条件
        obs1 = self.get_obs1()
        obs2 = self.get_obs2()
        # 分析reward
        if winner is None:
            reward1 = 0
            reward2 = 0
        elif winner is 1:
            reward1 = 1
            reward2 = -1
        elif winner is 2:
            reward1 = -1
            reward2 = 1
        else:
            reward1 = 0
            reward2 = 0
        return obs1, obs2, reward1, reward2, winner

    # 根据动作，环境做出相应的交互反应，人工输入参数的棋子序号是确定的，所以不需要分析
    def user_step(self, action_message):
        [user, piece_id, action] = action_message
        if user == 1:
            aim_piece = user1_piece[piece_id]
        else:
            aim_piece = user2_piece[piece_id]
        self.board.move_piece(aim_piece, action)
        #
        winner = self.board.is_Win()
        # 读取环境条件
        obs1 = self.get_obs1()
        obs2 = self.get_obs2()
        # 分析reward
        if winner is None:
            reward1 = 0
            reward2 = 0
        elif winner is 1:
            reward1 = 1
            reward2 = -1
        elif winner is 2:
            reward1 = -1
            reward2 = 1
        else:
            reward1 = 0
            reward2 = 0
        return obs1, obs2, reward1, reward2, winner

    # 主要调用app更新
    def refresh(self):
        self.app.show(self.board)
        self.app.update()

    # 输出函数，用于输出计算结果
    def show_winner(self, winner):
        self.iter_times += 1
        self.app.show_winner(self.board, winner)
        self.app.update()
        if self.queue.qsize() == 1000:
            self.queue.put(winner)
            ret = self.queue.get()
            if ret > winner:  # out 2 in 1
                self.win1_times += 1
            elif ret < winner:  # out 1 in 2
                self.win1_times -= 1
            all_time = 1000
        else:
            self.queue.put(winner)
            if winner == 1:
                self.win1_times += 1
            all_time = self.iter_times
        print("winner is ", winner, "     times", self.iter_times, "     rate:", self.win1_times / all_time)

    # -----------------------private----------------------------------------------#
    # 这一步的目的是去掉棋子的序号，将所有棋子看做是一样的，不同棋子位置相同则结果相同
    # 先将棋子按照位置排序，
    # action_message的[0:9]对应棋子位置最小的，
    # action_message的[9:18]对应棋子位置居中的，
    # action_message的[18:27]对应棋子位置最大的，
    def __analysis_action(self, action_message):
        # action_message = user, action
        user, act_index = action_message
        if user == 1:
            user_piece = user1_piece
        else:
            act_index = self.action_revserve(act_index)
            user_piece = user2_piece
        temp = [3 * p.pos[0] + p.pos[1] for p in user_piece]
        temp_sorted = sorted(temp)
        if act_index < 9:
            piece_id = temp.index(temp_sorted[0])
            action = self.action_space[act_index]
        elif act_index >= 18:
            piece_id = temp.index(temp_sorted[2])
            action = self.action_space[act_index - 18]
        else:
            piece_id = temp.index(temp_sorted[1])
            action = self.action_space[act_index - 9]
        return user, piece_id, action

    def user_action_to_com(self, action_message_for_user):
        [user, piece_id, action] = action_message_for_user
        if user == 1:
            user_piece = user1_piece
        else:
            user_piece = user2_piece
        temp = [3 * p.pos[0] + p.pos[1] for p in user_piece]
        temp_sorted = sorted(temp)
        pos = user_piece[piece_id].pos
        sorted_id = 0
        for value in temp_sorted:
            if 3 * pos[0] + pos[1] == value:
                sorted_id = temp_sorted.index(value)
        act_index = 9 * sorted_id + self.action_space.index(action)
        act_index = self.action_revserve(act_index)
        return user, act_index

    def get_obs1(self):
        obs = []
        for piece in user1_piece:
            obs.append(piece.pos)
        for piece in user2_piece:
            obs.append(piece.pos)
        return np.array(obs)

    def get_obs2(self):
        obs = []
        for piece in user2_piece:
            pos = piece.pos.copy()
            pos[0] = 2 - pos[0]
            pos[1] = 2 - pos[1]
            obs.append(pos)
        for piece in user1_piece:
            pos = piece.pos.copy()
            pos[0] = 2 - pos[0]
            pos[1] = 2 - pos[1]
            obs.append(pos)
        return np.array(obs)

    def obs_revserve(self, obs):
        pass

    def action_revserve(self, act_index):
        offset = 2 - act_index // 9
        act_ = self.action_space[act_index % 9]
        index = self.action_space.index(operate_reverse[act_])
        return offset * 9 + index

    def get_reward(self):
        pass


