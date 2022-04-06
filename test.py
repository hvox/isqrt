from isqrts import *
import multiprocessing
import time


def run_with_timeout(f, args, timeout):
    result_container = multiprocessing.Manager().list()
    result_container.append(None)
    result_container.append(timeout)

    def executer(result):
        t0 = time.time()
        try:
            result[0] = f(*args)
            result[1] = time.time() - t0
        except Exception as e:
            result[0] = str(e)
            result[1] = timeout

    ps = multiprocessing.Process(target=executer, args=(result_container,))
    ps.start()
    ps.join(timeout)
    result, delta = result_container
    if ps.is_alive():
        result = "TIMEOUT"
        ps.terminate()
    return result, delta


def test(name, f, x):
    # y0 = isqrt_py(x)
    y, delta = run_with_timeout(f, (x,), 0.1)
    return delta
    if y != y0:
        print("FAIL: ", name)
        print("returned:", x, "->", y)
        print(" correct:", x, "->", y0)
    return delta


def test_on_small_numbers(name, f):
    times = []
    for _ in range(10):
        times.append(test(name, f, randint(1, 10 ** 10)))
    return times


def test_on_big_numbers(name, f):
    times = []
    for _ in range(10):
        times.append(test(name, f, randint(1, 10 ** 80)))
    return times


def test_on_very_big_numbers(name, f):
    times = []
    for _ in range(10):
        times.append(test(name, f, randint(10 ** 400, 10 ** 800)))
    return times


from random import randint

times = {isqrt: [] for isqrt in isqrts}
for name, f in isqrts.items():
    times[name] += test_on_small_numbers(name, f)
    times[name] += test_on_big_numbers(name, f)
    times[name] += test_on_very_big_numbers(name, f)

print("--TIME--")
for name, ts in times.items():
    print(sum(ts) / len(ts), name)
