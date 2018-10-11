from chess.env import chess_env
from RL.q_learning import brain as RL
import numpy as np
import threading
import time


isbreak = 10


com1 = RL(1)
env = chess_env()
env.enable_control()
com1.load(name='data_log/q_table - save.npz')
def cal_loop():
    while True:
        # initial observation
        obs, obs1, obs2 = env.reset()
        action_message = None
        action_message2 = None
        while True:
            # fresh env 更新环境
            env.refresh()
            if isbreak: time.sleep(isbreak / 10)
            # RL choose action based on observation 根据当前环境选择动作
            action_message = com1.choose_action(env, obs, rate=1,isprint=True)
            # RL take action and get next observation and reward 根据计算出来的动作，更新环境，返回观测值，奖赏
            # 实际上这里只是参数的改变，真正的界面刷新在第一个更新环境
            obs1_, obs2_, reward1, reward2, winner = env.step(action_message)
            # 学习成功的经验
            com1.learn(obs, action_message, reward1, obs1_, winner)
            # 用对手的视角学习
            com1.learn(obs2, action_message2, reward2, obs1_, winner)
            # 保存对手的视角
            obs2 = obs2_
            if winner is not None:
                break
            env.refresh()
            if isbreak: time.sleep(isbreak / 10)
            action_message_for_user = env.wait_for_user()

            action_message2 = env.user_action_to_com( action_message_for_user)

            obs1_, obs2_, reward1, reward2, winner = env.user_step(action_message_for_user)
            # 学习失败的经验
            com1.learn(obs, action_message, reward1, obs1_, winner)
            # 用对手的视角学习
            com1.learn(obs2, action_message2, reward2, obs1_, winner)
            obs = obs1_
            # break while loop when end of this episode
            if winner is not None:
                break

        env.show_winner(winner)
        com1.save(name='data_log/q_table - save.npz')
        if isbreak: time.sleep(isbreak / 3)

cal_thread = threading.Thread(target=cal_loop, name='cal_loop')
cal_thread.start()
env.app.mainloop()

