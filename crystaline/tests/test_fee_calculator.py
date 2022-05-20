import pytest
from crystaline.fee_calculator import fee_calculator as fc

SIZE = 123
TIME_1 = 10
TIME_2 = 20
N = 4


def test_F_x():
    assert fc.F_x_calculator(SIZE) == 371


def test_H_x():
    assert fc.H_x_calculator(TIME_1, N, TIME_2) == 3.4828517376e+18
    assert fc.H_x_calculator(TIME_2, N, TIME_1) == 8.916100448256e+20


def test_K_x():
    assert fc.K_x_calculator(TIME_1, fc.BETA, SIZE) == 19.91902834008097


def test_G_x():
    assert fc.G_x_calculator(TIME_1, TIME_2, SIZE) == 860502.0242914979
