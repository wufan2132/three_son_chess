from sklearn import tree
import numpy as np


class brain(object):
    def __init__(self, user=1):
        self.alpha = 0.1  # 学习率
        self.gama = 0.5  # 对未来情况的衰减率
        self.q_table = {}
        self.action_nums = 3 * 9  # 动作空间数量
        self.user = user  # 此大脑的使用者id

    # -----------------------public----------------------------------------------#
    # 根据当前环境选择动作 rate：选择价值最高动作的概率， isprint：是否打印输出信息
    def choose_action(self, env, observation, rate=0.9, isprint=0):
        state = self.__pre_obs(observation)
        if state in self.q_table:  # 如果该状态已经存在
            # 获得可行解
            ave_vector = np.array(env.board.get_Feasible_operate_array(self.user))
            if isprint == 1:  # 打印q_table
                print("q_table: ", self.q_table[state])
            if np.random.choice([0, 1], p=[1 - rate, rate]) == 0:
                # 10%几率选择随机动作(在可行解中选择随机动作)
                [ave_index] = np.nonzero(ave_vector)
                action_index = np.random.choice(ave_index)
            else:
                # 90几率选择概率最大的动作
                action_index = self.__argmax(self.q_table[state], ave_vector)
        else:  # 如果不存在就随便选一个
            # self.q_table[state] = np.array([0.0] * 27)
            if isprint == 1:
                print("random ")
            ave_vector = np.array(env.board.get_Feasible_operate_array(self.user))
            [ave_index] = np.nonzero(ave_vector)
            action_index = np.random.choice(ave_index)
        return self.user, action_index

    # 根据一系列信息更新q_table
    def learn(self, observation, action_message, reward, observation_, winner):
        if action_message == None:
            return
        action = action_message[1]
        state = self.__pre_obs(observation)
        state_ = self.__pre_obs(observation_)
        if state in self.q_table.keys():
            q_predict = self.q_table[state][action]
        else:  # 如果不存在就新建一个
            self.q_table[state] = np.array([0.0] * 27)
            q_predict = 0
        if winner is None and state_ in self.q_table.keys():
            q_target = reward + self.gama * self.q_table[state_].max()
        else:
            q_target = reward
        self.q_table[state][action] += self.alpha * (q_target - q_predict)
        pass

    # 学习对手的经验也很重要
    def learn_reverse(self, observation, action_message, reward, observation_, winner):
        # 所有的obs在输出的之前已经转换成com1的视角
        pass

    # 打印q_table到txt文件
    def print_q_table(self, name='data_log/q_table.txt'):
        with open(name, 'w') as f:
            for num in self.q_table:
                string = "{0: <6}:".format(num)
                string += str(self.q_table[num])
                string += "\n"
                #
                f.write(string)
    # 保存q_table到npz文件
    def save(self, name='data_log/q_table.npz'):
        np.savez(name, dict=self.q_table)

    # 读取q_table的npz文件
    def load(self, name='data_log/q_table.npz'):
        data = np.load(name)
        self.q_table = data['dict'][()]

    # -----------------------private----------------------------------------------#
    # 选择可行解中值最大的动作，返回动作的index
    def __argmax(self, array, ave_vector):
        max = -np.inf
        max_index = -1
        for i in range(len(ave_vector)):
            if ave_vector[i] == True:
                if array[i] > max:
                    max = array[i]
                    max_index = i
        return max_index

    # 映射函数，将表示所有棋子的位置的6*2矩阵映射到一个数，不同序号同位置同阵营的棋子看做相同棋子
    def __pre_obs(self, observation):
        obs1 = observation[0:3, :]
        obs2 = observation[3:6, :]
        # 先对棋子按照位置排序，去掉棋子的id
        obs1_ = sorted(obs1, key=lambda i: 3 * i[0] + i[1])
        obs2_ = sorted(obs2, key=lambda i: 3 * i[0] + i[1])
        obs_mat = np.row_stack([obs1_, obs2_])
        # 将所有动作映射到一个数
        state = 0
        for a in obs_mat:
            state = state * 9 + 3 * a[0] + a[1]
        return state

    # 将数还原回到表示所有棋子的位置的6*2矩阵
    def __state_reverse(self, state):
        nums = []
        # 将数还原回来
        for i in range(12):
            nums.append(state % 3)
            state = (state - nums[-1]) // 3
        nums.reverse()
        mat = []
        for i in range(12):
            if i % 2 == 0:
                mat.append([])
                mat[-1].append(nums[i])
            else:
                mat[-1].append(nums[i])
        return mat
