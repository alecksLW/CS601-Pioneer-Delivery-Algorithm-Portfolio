# task_2a.py
# Task A: Closest Delivery Locations

import math

def parse_data(path):

    # Each line is structured as 'id x y'
    points = []
    with open(path) as f:
        for line in f:
            parts = line.split()

            # Use the first three entries
            if len(parts) >= 3:
                points.append((parts[0], int(parts[1]), int(parts[2])))
    return points


def parse_cases(path):

    # Each test case begins with a '# Test ...' line, followed by 'id x y' lines
    cases = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                cases.append((line[1:].strip(), []))
                continue

            parts = line.split()
            if len(parts) >= 3:
                cases[-1][1].append((parts[0], int(parts[1]), int(parts[2])))
    return cases


def sort(points, split):

    # Base case (one point)
    if len(points) <= 1:
        return points

    # Merge sort by the given coordinate (x, y), O(nlog(n))
    mid = len(points) // 2
    left = sort(points[:mid], split)
    right = sort(points[mid:], split)
    return merge(left, right, split)


def merge(left, right, split):
    merged = []
    i = 0
    j = 0

    # Keep merging until one side is exhausted
    while i < len(left) and j < len(right):
        if left[i][split] <= right[j][split]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append the rest of the entries
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def squared_dist(p, q):
    return (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2


def brute_force(points):
    best = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = squared_dist(points[i], points[j])
            if best is None or d < best[0]:
                best = (d, points[i], points[j])
    return best


def get_closest(sorted_x):

    # Brute force is only used for small cases
    if len(sorted_x) <= 3:
        return brute_force(sorted_x), sort(sorted_x, 2)

    mid = len(sorted_x) // 2
    mid_x = sorted_x[mid][1]

    # Recursively get the best left and right
    left_best, left_y = get_closest(sorted_x[:mid])
    right_best, right_y = get_closest(sorted_x[mid:])
    best = left_best if left_best[0] <= right_best[0] else right_best

    # Merge the sorted y's
    sorted_y = merge(left_y, right_y, 2)

    # Only points within the best distance of the center-split can form a closer pair
    center = []
    for point in sorted_y:
        if (point[1] - mid_x) ** 2 < best[0]:
            center.append(point)

    # Each center point is only compared with the next 7 points (in y)
    for i in range(len(center)):
        for j in range(i + 1, min(i + 8, len(center))):
            d = squared_dist(center[i], center[j])
            if d < best[0]:
                best = (d, center[i], center[j])
    return best, sorted_y


def closest_pair(points):
    
    # Error check: At least two locations are needed to form a pair
    if len(points) < 2:
        raise ValueError(f"Need at least two locations, got {len(points)}")

    best, _ = get_closest(sort(points, 1))
    d, p, q = best

    # List the pair in a consistent order (by x, then y)
    if (q[1], q[2]) < (p[1], p[2]):
        p, q = q, p
    return p[0], q[0], d


def run_req_cases(path):

    # Runs all the required/additional test cases from a file
    # If an error is encountered, return the error message
    for name, points in parse_cases(path):
        print(name)
        try:
            print_result(closest_pair(points))
        except ValueError as e:
            print(f" Error: {e}")
        print()


def print_result(result):
    dest1, dest2, total_dist = result
    print(f" Closest pair: {dest1}, {dest2}")
    print(f" Squared distance: {total_dist}")
    print(f" Distance: {math.sqrt(total_dist):.4f}")


if __name__ == "__main__":

    # Runs the algorithm from a file
    print_result(closest_pair(parse_data("./data/locations.txt")))
    print()

    # Runs all required and additional test cases
    run_req_cases("./data/test_cases_2a.txt")