from crystaline.public_address.public_address_generator import PublicAddressGenerator
import time

if __name__ == "__main__":
    t0 = time.time()
    TESTS = 1001
    for i in range(1, TESTS):
        generator = PublicAddressGenerator(i)
    t1 = time.time()
    print(t1 - t0)
