# task_2c.py
# Task C: Selecting a Delivery-Time Threshold

def parse_cases(path):

    # Each test case begins with a '# Test ...' line, followed by a 'T:' line and a 'k:' line
    cases = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                cases.append([line[1:].strip(), [], 0])
            elif line.startswith("T:"):
                cases[-1][1] = [int(t) for t in line.split(":")[1].split()]
            elif line.startswith("k:"):
                cases[-1][2] = int(line.split(":")[1])
    return cases


def select(values, k):

    # Base case (small array, sorting at most five elements is allowed)
    if len(values) <= 5:
        return sorted(values)[k - 1]

    # Split into groups of at most five and take the median of each group
    medians = []
    for i in range(0, len(values), 5):
        group = sorted(values[i:i + 5])
        medians.append(group[(len(group) - 1) // 2])

    # The pivot is the median of the group medians (found recursively)
    pivot = select(medians, (len(medians) + 1) // 2)

    # Partition into values less than, equal to, and greater than the pivot
    less = []
    equal = []
    greater = []
    for value in values:
        if value < pivot:
            less.append(value)
        elif value == pivot:
            equal.append(value)
        else:
            greater.append(value)

    # Only recurse into the group that contains rank k
    if k <= len(less):
        return select(less, k)
    if k <= len(less) + len(equal):
        return pivot

    # Skip past the less and equal groups, so k is now a rank within greater
    return select(greater, k - len(less) - len(equal))


def get_kth_smallest(times, k):

    # Error handling (>0 times, nonnegative times, 1 <= k <= n)
    if len(times) == 0:
        raise ValueError("Need at least one delivery time")
    if min(times) < 0:
        raise ValueError("Delivery times must be nonnegative")
    if k < 1 or k > len(times):
        raise ValueError(f"k must be between 1 and {len(times)}, but we got {k}")

    return select(times, k)


def run_req_cases(path):

    # Runs all the required/additional test cases from a file
    for name, times, k in parse_cases(path):
        print(name)
        print(f" T = [{', '.join(str(t) for t in times)}]")
        print(f" k = {k}")
        try:
            print_result(get_kth_smallest(times, k))
        except ValueError as e:
            print(f" Error: {e}")
        print()


def print_result(value):
    print(f" kth smallest value: {value}")


if __name__ == "__main__":

    # Runs all required and additional test cases
    run_req_cases("./data/test_cases_2c.txt")