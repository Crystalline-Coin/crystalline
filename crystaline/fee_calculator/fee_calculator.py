import time
from ..blockchain import Blockchain



TIME_PERIOD = 30                                                                  #time_period : t
ALPHA = 2
N = 1
BETA = 20


def F_x_calculator(alpha , uploaded_file_size):                                  # uploaded_file_size : S_c
    F_x = uploaded_file_size * alpha + alpha        
    for i in range(0 , int(uploaded_file_size)):                                 # applying floors
        F_x += 1
    return F_x

def H_x_calculator(time_period , n , times_diffrence):                                   
    time_period = time_period * 24 * 60 * 60
    H_x = 0
    if(times_diffrence <= time_period):
        H_x = pow(time_period/times_diffrence , n)
    else:
        H_x = 1
    return H_x

def K_x_calculator(time_period , beta , file_size):                               #file size: s
    k_x = -(time_period/(file_size+(time_period/beta))) + beta
    return k_x

def G_x_calculator(times_diffrence , file_size):
    return K_x_calculator(file_size) * H_x_calculator(times_diffrence)