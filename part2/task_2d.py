# task_2d.py
# Task D: Validation and Algorithm Analysis (reference checks and timings)

import random
import time

from task_2a import closest_pair, squared_dist
from task_2b import get_total_inversions
from task_2c import get_kth_smallest



def reference_closest(points):

    # Brute force: compare every pair
    best = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = squared_dist(points[i], points[j])
            if best is None or d < best:
                best = d
    return best


def reference_inversions(planned, actual):

    # Two nested loops: count pairs that are in opposite order
    position = {}
    for i, id in enumerate(actual):
        position[id] = i

    count = 0
    for i in range(len(planned)):
        for j in range(i + 1, len(planned)):
            if position[planned[i]] > position[planned[j]]:
                count += 1
    return count


def reference_kth(times, k):

    # Sort everything and take the kth entry
    return sorted(times)[k - 1]


# Correctness checks
def check_closest(trials):

    # A small coordinate range forces many ties in x and in distance
    cells = [(x, y) for x in range(-10, 11) for y in range(-10, 11)]
    matched = 0
    for _ in range(trials):
        coords = random.sample(cells, random.randint(2, 30))
        points = [(f"P{i}", x, y) for i, (x, y) in enumerate(coords)]
        lookup = {p[0]: p for p in points}

        id1, id2, d = closest_pair(points)

        # The distance must be minimal, and the returned IDs must really have that distance
        if d == reference_closest(points) == squared_dist(lookup[id1], lookup[id2]):
            matched += 1
    print(f"Task A: {matched}/{trials} matched brute force")


def check_inversions(trials):
    matched = 0
    for _ in range(trials):
        n = random.randint(1, 30)
        planned = list(range(n))
        actual = planned[:]
        random.shuffle(actual)

        if get_total_inversions(planned, actual) == reference_inversions(planned, actual):
            matched += 1
    print(f"Task B: {matched}/{trials} matched nested loops")


def check_select(trials):

    # A small value range forces many duplicates
    matched = 0
    for _ in range(trials):
        n = random.randint(1, 60)
        times = [random.randint(0, random.choice([3, 10, 1000])) for _ in range(n)]
        k = random.randint(1, n)

        if get_kth_smallest(times, k) == reference_kth(times, k):
            matched += 1
    print(f"Task C: {matched}/{trials} matched sorting")


# Timings (for the report)
def make_points(n):

    # n distinct random locations
    seen = set()
    points = []
    while len(points) < n:
        x = random.randint(0, 10 * n)
        y = random.randint(0, 10 * n)
        if (x, y) not in seen:
            seen.add((x, y))
            points.append((f"P{len(points)}", x, y))
    return points


def best_time(func, runs=3):

    # Best of several runs, in seconds
    best = None
    for _ in range(runs):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        if best is None or elapsed < best:
            best = elapsed
    return best


def time_task(name, sizes, make_input, run):
    print(name)
    print(f" {'n':>8} {'time (s)':>10} {'growth':>8}")
    previous = None
    for n in sizes:
        data = make_input(n)
        seconds = best_time(lambda: run(data))
        growth = "" if previous is None else f"{seconds / previous:.1f}x"
        print(f" {n:>8} {seconds:>10.4f} {growth:>8}")
        previous = seconds
    print()


def make_orders(n):
    planned = list(range(n))
    actual = planned[:]
    random.shuffle(actual)
    return planned, actual


def make_times(n):
    return [random.randint(0, 1000000) for _ in range(n)]


if __name__ == "__main__":
    random.seed(0)

    # Compares each algorithm with its simple reference solution
    print("Correctness checks")
    check_closest(2000)
    check_inversions(2000)
    check_select(2000)
    print()

    # Times each algorithm on three increasing input sizes (the median k is used for Task C)
    sizes = [1000, 10000, 100000]
    print("Timings (best of 3 runs)")
    time_task("Task A: closest pair", sizes, make_points, closest_pair)
    time_task("Task B: inversions", sizes, make_orders, lambda data: get_total_inversions(*data))
    time_task("Task C: kth smallest", sizes, make_times, lambda data: get_kth_smallest(data, len(data) // 2))