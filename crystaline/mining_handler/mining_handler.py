import math

MIDDLE_OF_64_BYTE_HASHES = 0x8000000000000000000000000000000000000000000000000000000000000000  # 5.78960446186581 * pow(10,76)
WANTED_AVERAGE_MINING_TIME = float  # by minute
MAX_OF_BOOSTER = float  # number must put manually
MAX_OF_POSSIBLE_STAKE_X_TIMEWEIGHT = float
GROWTH_LENGTH_STAIR = float
DEFAULT_UPLOADED_FILE_SIZE_COEFF = float
DEFAULT_Y_INTERCEPT_COEFF = float
DEFAULT_X_INTERCEPT_COEFF = float

def mining_equation(
    miner_founded_hash,
    user_utxo,
    user_utxo_timeweight,
    current_average_time_of_mining,
    user_address,
    miner_all_uploaded_files_size,
):
    difficulty = current_average_time_of_mining / WANTED_AVERAGE_MINING_TIME
    booster = booster_calculator(user_utxo, user_utxo_timeweight)
    right_side_of_equation = MIDDLE_OF_64_BYTE_HASHES * difficulty * booster
    if miner_founded_hash <= right_side_of_equation:
        return True
    else:
        return False

def booster_calculator(user_utxo, user_utxo_timeweight, miner_all_uploaded_files_size):
    x = user_utxo * user_utxo_timeweight
    y = 1 + ((MAX_OF_BOOSTER - 1) / MAX_OF_POSSIBLE_STAKE_X_TIMEWEIGHT) * x

    all_stairs_count = 0
    max_x = MAX_OF_POSSIBLE_STAKE_X_TIMEWEIGHT
    while max_x < GROWTH_LENGTH_STAIR:
        max_x - GROWTH_LENGTH_STAIR
        all_stairs_count += 1

    x_stairs_count = 0
    while x < GROWTH_LENGTH_STAIR:
        x - GROWTH_LENGTH_STAIR
        x_stairs_count += 1

    booster = (
        1 + ((y - 1) / all_stairs_count) * x_stairs_count
    )
    return booster

def POA_factor(miner_all_uploaded_files_size):
    POA_Coefficient = math.tanh(uploaded_files_size_coefficient() * miner_all_uploaded_files_size - x_intercept_coefficient()) + y_intercept_coefficient()
    
def uploaded_files_size_coefficient():
    return DEFAULT_UPLOADED_FILE_SIZE_COEFF

def y_intercept_coefficient():
    return DEFAULT_Y_INTERCEPT_COEFF

def x_intercept_coefficient():
    return DEFAULT_X_INTERCEPT_COEFF
    
