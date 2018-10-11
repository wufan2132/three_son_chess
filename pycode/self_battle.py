from chess.env import chess_env
from RL.q_learning import brain as RL
import numpy as np
import threading
import time

isbreak = 0


com1 = RL(1)
# com2 = RL(2)
env = chess_env()
com1.load()
def cal_loop():
    for episode in range(10000):
        # initial observation
        obs, obs1, obs2 = env.reset()

        while True:
            if isbreak: time.sleep(isbreak/10)
            # fresh env 更新环境
            env.refresh()
            # RL choose action based on observation 根据当前环境选择动作
            action_message = com1.choose_action(env, obs, rate=1)
            # RL take action and get next observation and reward 根据计算出来的动作，更新环境，返回观测值，奖赏
            # 实际上这里只是参数的改变，真正的界面刷新在第一个更新环境
            obs1_, obs2_, reward1, reward2, winner = env.step(action_message)
            # RL learn from this transition 根据观测值更新Q_table
            com1.learn(obs, action_message, reward1, obs1_, winner)
            # swap observation
            obs1 = obs1_
            obs = obs1_
            obs2 = obs2_
            # break while loop when end of this episode
            if winner is not None:
                break
            if isbreak: time.sleep(isbreak/10)
            # fresh env 更新环境
            env.refresh()
            # RL choose action based on observation 根据环境选择动作
            action_message2 = com1.choose_action(env, obs2)
            # RL take action and get next observation and reward 根据计算出来的动作，更新环境，返回观测值，奖赏
            # 实际上这里只是参数的改变，真正的界面刷新在第一个更新环境
            obs1_, obs2_, reward1, reward2, winner = env.step(action_message2)
            # RL learn from this transition 根据观测值更新Q_table
            com1.learn(obs2, action_message2, reward2, obs2_, winner)
            # swap observation
            obs = obs1_
            obs2 = obs2_
            # break while loop when end of this episode
            if winner is not None:
                break

        env.show_winner(winner)
        if isbreak:
            time.sleep(isbreak/3)
        if episode%1000 == 0:
            com1.print_q_table()
            com1.save()
        pass





cal_thread = threading.Thread(target=cal_loop, name='cal_loop')
cal_thread.start()
env.app.mainloop()



