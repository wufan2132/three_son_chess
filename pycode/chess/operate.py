
# 定义一些函数和变量用dict映射，为了代码简洁，用空间换取时间
def up(a):
    a[0] -= 1
    return a

def down(a):
    a[0] += 1
    return a

def left(a):
    a[1] -= 1
    return a

def right(a):
    a[1] += 1
    return a

def center(a):
    a[0] = 1
    a[1] = 1
    return a

def up_left(a):
    a[0] -= 1
    a[1] -= 1
    return a

def down_left(a):
    a[0] += 1
    a[1] -= 1
    return a


def up_right(a):
    a[0] -= 1
    a[1] += 1
    return a


def down_right(a):
    a[0] += 1
    a[1] += 1
    return a


operate_dict = {
    "up": up,
    "down": down,
    "left": left,
    "right": right,
    "center": center,
    "up_left": up_left,
    "down_left": down_left,
    "up_right": up_right,
    "down_right": down_right
}

operate_reverse = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
    "center": "center",
    "up_left": "down_right",
    "down_left": "up_right",
    "up_right":"down_left",
    "down_right": "up_left"
}
