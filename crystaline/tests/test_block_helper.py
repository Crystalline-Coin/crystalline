import pytest

from ..block.helper import gen_hash_encoded, gen_hash
from ..block.helper import __calc_block_reward_i, __calc_block_reward_R_i, __calc_reward
import math


def test_block_hash_generation1():
    data_str = "18c05d189f44e7a5dd7124d6f4d3c9a9802bf7b647c1d5ae295d35e5be5d7772"
    exp_res = "aea10f6c1dd2321e8c8bb5037efc45e2c01b2e55949c1718ab5e72cf82642c74cab04da15b319054fdfcab4f650a8765"
    assert gen_hash(data_str) == exp_res


def test_block_hash_generation2():
    data_str = "18c05d189f44e7a5dd7124d6f4d3c9a9802bf7b647c1d5ae295d35e5be5d7772"
    exp_res = "aea10f6c1dd2321e8c8bb5037efc45r2c01b2e55949c1718ab5e72cf82642c74cab04da15b319054fdfcab4f650a8765"
    assert gen_hash(data_str) != exp_res


def test_block_hash_generation_encoded1():
    data_str = "18d7c272f74122eeeaa0316416c11809438d7e5f171146f3f618a1ecd321358678140cf97bc8ea759e13b75bfb00a272ebec8c75ae9c2048960693ad323662de"
    exp_res = "373de55a59c614bee9a08d430d8169e93663527505bebe786dbe7b521b578db446f5b66fc4c0ff01f66ff0ede839448f"
    assert gen_hash_encoded(bytearray(data_str, encoding="utf-8")) == exp_res


def test_block_hash_generation_encoded2():
    data_str = "18d7c272f74122eeeaa0316416c11809438d7e5f171146f3f618a1ecd321358678140cf97bc8ea759e13b75bfb00a272ebec8c75ae9c2048960693ad323662de"
    exp_res = "373de55a59c614bee9a08d430d8169e93663527505bebe786dbe7b521b578db446f5b66fc4c0ff01f66ff0ede839448e"
    assert gen_hash_encoded(bytearray(data_str, encoding="utf-8")) != exp_res


@pytest.mark.slow
def test_block_reward1():
    # consts
    T = 12
    R = 50

    expected_output = [
        3.1927262e-01,
        7.6020800e-03,
        1.0549460e-02,
        1.4639540e-02,
        2.0315390e-02,
        2.8191790e-02,
        3.9121910e-02,
        5.4289720e-02,
        7.5338180e-02,
        1.0454726e-01,
        1.4508087e-01,
        2.0132962e-01,
        2.7938635e-01,
        1.1997750e-02,
        1.5740340e-02,
        2.0650410e-02,
        2.7092120e-02,
        3.5543280e-02,
        4.6630700e-02,
        6.1176750e-02,
        8.0260310e-02,
        1.0529682e-01,
        1.3814327e-01,
        1.8123587e-01,
        2.3777085e-01,
        1.7941370e-02,
        2.2286920e-02,
        2.7685000e-02,
        3.4390540e-02,
        4.2720220e-02,
        5.3067420e-02,
        6.5920790e-02,
        8.1887360e-02,
        1.0172118e-01,
        1.2635891e-01,
        1.5696410e-01,
        1.9498213e-01,
        2.4757460e-02,
        2.9201210e-02,
        3.4442580e-02,
        4.0624730e-02,
        4.7916530e-02,
        5.6517140e-02,
        6.6661490e-02,
        7.8626660e-02,
        9.2739480e-02,
        1.0938544e-01,
        1.2901920e-01,
        1.5217705e-01,
        3.0386440e-02,
        3.4195200e-02,
        3.8481370e-02,
        4.3304780e-02,
        4.8732780e-02,
        5.4841140e-02,
        6.1715160e-02,
        6.9450790e-02,
        7.8156030e-02,
        8.7952430e-02,
        9.8976740e-02,
        1.1138289e-01,
        3.1832870e-02,
        3.4429530e-02,
        3.7238000e-02,
        4.0275570e-02,
        4.3560920e-02,
        4.7114260e-02,
        5.0957450e-02,
        5.5114140e-02,
        5.9609890e-02,
        6.4472370e-02,
        6.9731490e-02,
        7.5419610e-02,
        2.7669150e-02,
        2.9032840e-02,
        3.0463740e-02,
        3.1965170e-02,
        3.3540590e-02,
        3.5193660e-02,
        3.6928200e-02,
        3.8748230e-02,
        4.0657970e-02,
        4.2661820e-02,
        4.4764440e-02,
        4.6970680e-02,
        2.0034500e-02,
        2.0592680e-02,
        2.1166400e-02,
        2.1756100e-02,
        2.2362240e-02,
        2.2985260e-02,
        2.3625640e-02,
        2.4283860e-02,
        2.4960420e-02,
        2.5655830e-02,
        2.6370620e-02,
        2.7105320e-02,
        1.2530930e-02,
        1.2718620e-02,
        1.2909120e-02,
        1.3102480e-02,
        1.3298730e-02,
        1.3497930e-02,
        1.3700110e-02,
        1.3905310e-02,
        1.4113590e-02,
        1.4324990e-02,
        1.4539550e-02,
        1.4757330e-02,
        7.1014900e-03,
        7.1568400e-03,
        7.2126300e-03,
        7.2688500e-03,
        7.3255100e-03,
        7.3826200e-03,
        7.4401600e-03,
        7.4981600e-03,
        7.5566100e-03,
        7.6155100e-03,
        7.6748800e-03,
        7.7347000e-03,
        3.7953700e-03,
        3.8104800e-03,
        3.8256500e-03,
        3.8408800e-03,
        3.8561600e-03,
        3.8715200e-03,
        3.8869300e-03,
        3.9024000e-03,
        3.9179300e-03,
        3.9335300e-03,
        3.9491900e-03,
        3.9649100e-03,
        1.9641400e-03,
        1.9680900e-03,
        1.9720500e-03,
        1.9760200e-03,
        1.9799900e-03,
        1.9839800e-03,
        1.9879700e-03,
        1.9919700e-03,
        1.9959800e-03,
        1.9999900e-03,
        2.0040200e-03,
        2.0080500e-03,
        9.9941000e-04,
        1.0004200e-03,
        1.0014300e-03,
        1.0024400e-03,
        1.0034600e-03,
        1.0044700e-03,
        1.0054900e-03,
        1.0065000e-03,
        1.0075200e-03,
        1.0085400e-03,
        1.0095600e-03,
        1.0105800e-03,
        5.0413000e-04,
        5.0439000e-04,
        5.0464000e-04,
        5.0490000e-04,
        5.0516000e-04,
        5.0541000e-04,
        5.0567000e-04,
        5.0592000e-04,
        5.0618000e-04,
        5.0644000e-04,
        5.0669000e-04,
        5.0695000e-04,
        2.5319000e-04,
        2.5325000e-04,
        2.5331000e-04,
        2.5338000e-04,
        2.5344000e-04,
        2.5351000e-04,
        2.5357000e-04,
        2.5364000e-04,
        2.5370000e-04,
        2.5376000e-04,
        2.5383000e-04,
        2.5389000e-04,
        1.2687000e-04,
        1.2689000e-04,
        1.2691000e-04,
        1.2692000e-04,
        1.2694000e-04,
        1.2695000e-04,
        1.2697000e-04,
        1.2699000e-04,
        1.2700000e-04,
        1.2702000e-04,
        1.2704000e-04,
        1.2705000e-04,
        6.3510000e-05,
        6.3510000e-05,
        6.3520000e-05,
        6.3520000e-05,
        6.3520000e-05,
        6.3530000e-05,
        6.3530000e-05,
        6.3540000e-05,
        6.3540000e-05,
        6.3540000e-05,
        6.3550000e-05,
        6.3550000e-05,
        3.1770000e-05,
        3.1770000e-05,
        3.1770000e-05,
        3.1770000e-05,
        3.1780000e-05,
        3.1780000e-05,
        3.1780000e-05,
        3.1780000e-05,
        3.1780000e-05,
        3.1780000e-05,
        3.1780000e-05,
        3.1780000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        1.5890000e-05,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        7.9500000e-06,
        3.9700000e-06,
        3.9700000e-06,
        3.9700000e-06,
        3.9700000e-06,
        3.9700000e-06,
        3.9700000e-06,
        3.9700000e-06,
        3.9700000e-06,
        3.9700000e-06,
    ]

    for n in range(1, 250):
        i = __calc_block_reward_i(n, T)
        R_i = __calc_block_reward_R_i(R, i)
        assert round(__calc_reward(n, R_i, T, i), 8) == expected_output[n]


@pytest.mark.slow
def test_block_reward2():
    # consts
    T = 250
    R = 100

    expected_output = [
        0.0209898,
        0.00018447,
        0.00018791,
        0.00019141,
        0.00019498,
        0.00019861,
        0.00020231,
        0.00020608,
        0.00020992,
        0.00021383,
        0.00021782,
        0.00022188,
        0.00022601,
        0.00023022,
        0.00023451,
        0.00023888,
        0.00024333,
        0.00024786,
        0.00025248,
        0.00025719,
        0.00026198,
        0.00026686,
        0.00027183,
        0.0002769,
        0.00028206,
        0.00028731,
        0.00029266,
        0.00029812,
        0.00030367,
        0.00030933,
        0.00031509,
        0.00032096,
        0.00032694,
        0.00033303,
        0.00033924,
        0.00034556,
        0.000352,
        0.00035856,
        0.00036524,
        0.00037204,
        0.00037898,
        0.00038604,
        0.00039323,
        0.00040056,
        0.00040802,
        0.00041562,
        0.00042336,
        0.00043125,
        0.00043929,
        0.00044747,
        0.00045581,
        0.0004643,
        0.00047295,
        0.00048177,
        0.00049074,
        0.00049988,
        0.0005092,
        0.00051869,
        0.00052835,
        0.00053819,
        0.00054822,
        0.00055844,
        0.00056884,
        0.00057944,
        0.00059024,
        0.00060123,
        0.00061244,
        0.00062385,
        0.00063547,
        0.00064731,
        0.00065937,
        0.00067166,
        0.00068417,
        0.00069692,
        0.0007099,
        0.00072313,
        0.0007366,
        0.00075033,
        0.00076431,
        0.00077855,
        0.00079305,
        0.00080783,
        0.00082288,
        0.00083821,
        0.00085383,
        0.00086974,
        0.00088594,
        0.00090245,
        0.00091926,
        0.00093639,
        0.00095384,
        0.00097161,
        0.00098971,
        0.00100815,
        0.00102694,
        0.00104607,
        0.00106556,
        0.00108542,
        0.00110564,
        0.00112624,
        0.00114722,
        0.0011686,
        0.00119037,
        0.00121255,
        0.00123514,
        0.00125816,
        0.0012816,
        0.00130548,
        0.0013298,
        0.00135458,
        0.00137981,
        0.00140552,
        0.00143171,
        0.00145839,
        0.00148556,
        0.00151324,
        0.00154143,
        0.00157015,
        0.00159941,
        0.00162921,
        0.00165956,
        0.00169048,
        0.00172198,
        0.00175406,
        0.00178675,
        0.00182004,
        0.00185395,
        0.00188849,
        0.00192368,
        0.00195952,
        0.00199603,
        0.00203322,
        0.0020711,
        0.00210969,
        0.002149,
        0.00218904,
        0.00222982,
        0.00227137,
        0.00231369,
        0.0023568,
        0.00240071,
        0.00244544,
        0.002491,
        0.00253741,
        0.00258469,
        0.00263285,
        0.0026819,
        0.00273187,
        0.00278277,
        0.00283462,
        0.00288743,
        0.00294123,
        0.00299603,
        0.00305185,
        0.00310872,
        0.00316664,
        0.00322564,
        0.00328574,
        0.00334696,
        0.00340932,
        0.00347284,
        0.00353755,
        0.00360346,
        0.0036706,
        0.00373899,
        0.00380865,
        0.00387961,
        0.0039519,
        0.00402553,
        0.00410053,
        0.00417694,
        0.00425476,
        0.00433403,
        0.00441479,
        0.00449704,
        0.00458083,
        0.00466618,
        0.00475312,
        0.00484168,
        0.00493189,
        0.00502378,
        0.00511738,
        0.00521273,
        0.00530985,
        0.00540879,
        0.00550956,
        0.00561221,
        0.00571678,
        0.0058233,
        0.0059318,
        0.00604232,
        0.0061549,
        0.00626957,
        0.00638639,
        0.00650538,
        0.00662659,
        0.00675005,
        0.00687582,
        0.00700393,
        0.00713443,
        0.00726735,
        0.00740276,
        0.00754069,
        0.00768118,
        0.0078243,
        0.00797008,
        0.00811858,
        0.00826984,
        0.00842393,
        0.00858088,
        0.00874076,
        0.00890362,
        0.00906951,
        0.00923849,
        0.00941062,
        0.00958596,
        0.00976456,
        0.0099465,
        0.01013182,
        0.01032059,
        0.01051289,
        0.01070876,
        0.01090829,
        0.01111153,
        0.01131856,
        0.01152945,
        0.01174426,
        0.01196308,
        0.01218597,
        0.01241302,
        0.0126443,
        0.01287989,
        0.01311987,
        0.01336432,
        0.01361332,
        0.01386696,
        0.01412533,
        0.01438851,
        0.0146566,
        0.01492968,
        0.01520785,
        0.0154912,
        0.01577983,
        0.01607384,
        0.01637332,
        0.01667839,
        0.01698914,
        0.01730568,
        0.01762812,
        0.01795657,
        0.01829113,
        0.00031082,
        0.00031574,
        0.00032075,
        0.00032583,
        0.000331,
        0.00033624,
        0.00034157,
        0.00034699,
        0.00035249,
        0.00035808,
        0.00036375,
        0.00036952,
        0.00037538,
        0.00038133,
        0.00038737,
        0.00039351,
        0.00039975,
        0.00040609,
        0.00041252,
        0.00041906,
        0.00042571,
        0.00043245,
        0.00043931,
        0.00044627,
        0.00045335,
        0.00046053,
        0.00046783,
        0.00047525,
        0.00048278,
        0.00049044,
        0.00049821,
        0.00050611,
        0.00051413,
        0.00052228,
        0.00053056,
        0.00053897,
        0.00054751,
        0.00055619,
        0.00056501,
        0.00057396,
        0.00058306,
        0.0005923,
        0.00060169,
        0.00061123,
        0.00062092,
        0.00063076,
        0.00064076,
        0.00065092,
        0.00066124,
        0.00067172,
        0.00068237,
        0.00069318,
        0.00070417,
        0.00071533,
        0.00072667,
        0.00073819,
        0.00074989,
        0.00076178,
        0.00077386,
        0.00078612,
        0.00079858,
        0.00081124,
        0.0008241,
        0.00083717,
        0.00085044,
        0.00086392,
        0.00087761,
        0.00089152,
        0.00090565,
        0.00092001,
        0.00093459,
        0.00094941,
        0.00096446,
        0.00097975,
        0.00099528,
        0.00101105,
        0.00102708,
        0.00104336,
        0.0010599,
        0.0010767,
        0.00109377,
        0.00111111,
        0.00112872,
        0.00114661,
        0.00116479,
        0.00118325,
        0.00120201,
        0.00122106,
        0.00124042,
        0.00126008,
        0.00128006,
        0.00130035,
        0.00132096,
        0.0013419,
        0.00136317,
        0.00138478,
        0.00140673,
        0.00142903,
        0.00145168,
        0.00147469,
        0.00149807,
        0.00152182,
        0.00154594,
        0.00157044,
        0.00159534,
        0.00162063,
        0.00164632,
        0.00167241,
        0.00169892,
        0.00172585,
        0.00175321,
        0.001781,
        0.00180924,
        0.00183791,
        0.00186705,
        0.00189664,
        0.00192671,
        0.00195725,
        0.00198828,
        0.00201979,
        0.00205181,
        0.00208434,
        0.00211738,
        0.00215094,
        0.00218504,
        0.00221967,
        0.00225486,
        0.0022906,
        0.00232691,
        0.0023638,
        0.00240127,
        0.00243933,
        0.002478,
        0.00251728,
        0.00255718,
        0.00259772,
        0.00263889,
        0.00268072,
        0.00272322,
        0.00276639,
        0.00281024,
        0.00285478,
        0.00290004,
        0.00294601,
        0.00299271,
        0.00304015,
        0.00308834,
        0.00313729,
        0.00318702,
        0.00323754,
        0.00328886,
        0.003341,
        0.00339396,
        0.00344776,
        0.00350241,
        0.00355793,
        0.00361433,
        0.00367162,
        0.00372982,
        0.00378895,
        0.00384901,
        0.00391002,
        0.003972,
        0.00403496,
        0.00409892,
        0.0041639,
        0.0042299,
        0.00429695,
        0.00436507,
        0.00443426,
        0.00450455,
        0.00457595,
        0.00464849,
        0.00472218,
        0.00479703,
        0.00487307,
        0.00495032,
        0.00502879,
        0.0051085,
        0.00518948,
        0.00527174,
        0.00535531,
        0.0054402,
        0.00552643,
        0.00561404,
        0.00570303,
        0.00579343,
        0.00588527,
        0.00597856,
        0.00607333,
        0.0061696,
        0.0062674,
        0.00636675,
        0.00646767,
        0.00657019,
        0.00667434,
        0.00678014,
        0.00688762,
        0.0069968,
        0.00710771,
        0.00722038,
        0.00733483,
        0.0074511,
        0.00756921,
        0.0076892,
        0.00781108,
        0.0079349,
        0.00806068,
        0.00818846,
        0.00831826,
        0.00845012,
        0.00858406,
        0.00872013,
        0.00885836,
        0.00899878,
        0.00914143,
        0.00928633,
        0.00943354,
        0.00958307,
        0.00973498,
        0.0098893,
        0.01004606,
        0.01020531,
        0.01036708,
        0.01053141,
        0.01069835,
        0.01086794,
        0.01104021,
        0.01121522,
        0.011393,
        0.01157359,
        0.01175705,
        0.01194342,
        0.01213275,
        0.01232507,
        0.01252044,
        0.01271891,
        0.01292053,
        0.01312534,
        0.0133334,
        0.01354475,
        0.01375946,
        0.01397757,
        0.01419914,
        0.01442421,
        0.01465286,
        0.01488513,
        0.01512109,
        0.01536078,
    ]

    for n in range(1, 500):
        i = __calc_block_reward_i(n, T)
        R_i = __calc_block_reward_R_i(R, i)
        assert round(__calc_reward(n, R_i, T, i), 8) == expected_output[n]
