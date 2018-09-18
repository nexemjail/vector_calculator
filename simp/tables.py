X = 'X'
D = 'D'
NOT_D = '~D'


def f1(x1, x2):
    return not (x1 & x2)


def f2(x3):
    return not x3


def f3(x5, x6):
    return not (x5 | x6)


def f4(x4, out_f3, x7):
    return not (x4 & out_f3 & x7)


def f5(out_f2, out_f4):
    return out_f2 ^ out_f4


def f6(out_f1, out_f5):
    return out_f1 & out_f5


f1_table = [
    [True, True, False],
    [False, X, True],
    [X, False, True],
    [False, False, True]
]

f2_table = [
    [True, False],
    [False, True]
]

f3_table = [
    [True, X, False],
    [X, True, False],
    [False, False, True]
]

f4_table = [
    [True, True, True, False],
    [False, X, X, True],
    [X, False, X, True],
    [X, X, False, True],
]

f5_table = [
    [False, False, False],
    [False, True, True],
    [True, False, True],
    [True, True, False]
]

f6_table = [
    [True, True, True],
    [False, X, False],
    [X, False, False]
]