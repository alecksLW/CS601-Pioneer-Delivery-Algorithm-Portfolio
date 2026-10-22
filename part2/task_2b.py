# task_2b.py
# Task B: Counting Dispatch-Order Inversions

def parse_cases(path):

    # Each test case begins with a '# Test ...' line, followed by a planned and actual line
    cases = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                cases.append([line[1:].strip(), [], []])
            elif line.startswith("planned:"):
                cases[-1][1] = line.split(":")[1].split()
            elif line.startswith("actual:"):
                cases[-1][2] = line.split(":")[1].split()
    return cases


def get_ranks(planned, actual):

    # Error handling (>0 deliveries, mismatched lengths, repeating IDs, mismatched IDs)
    if len(planned) == 0:
        raise ValueError("Error: Need at least one delivery")
    if len(planned) != len(actual):
        raise ValueError(f"Error: Planned and actual have different sizes ({len(planned)} and {len(actual)})")
    if len(set(planned)) != len(planned) or len(set(actual)) != len(actual):
        raise ValueError("Error: Each delivery ID must appear exactly once")
    if set(planned) != set(actual):
        raise ValueError("Error: Planned and actual must contain the same delivery IDs")

    # Calculate each delivery's rank
    rank = {}
    for i, id in enumerate(planned):
        rank[id] = i + 1

    # Return the rank for each ID
    return [rank[id] for id in actual]


def count_inversions(ranks):

    # Base case (0 or 1 element(s), no inversions)
    if len(ranks) <= 1:
        return ranks, 0

    mid = len(ranks) // 2

    # Count the number of inversions in the left and right halves
    left, left_count = count_inversions(ranks[:mid])
    right, right_count = count_inversions(ranks[mid:])

    # Count the number of inversions that cross mid
    merged, cross_count = merge_count(left, right)

    # Total inversions = left half + right half + crosses mid
    return merged, left_count + right_count + cross_count


def merge_count(left, right):
    merged = []
    count = 0
    i = 0
    j = 0

    # Keep merging until one side is exhausted
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])

            # right[j] < all remaining left elements, so count each as an inversion
            j += 1
            count += len(left) - i

    # Append the rest of the entries
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, count


def get_total_inversions(planned, actual):
    _, count = count_inversions(get_ranks(planned, actual))
    return count


def run_req_cases(path):

    # Runs all the required/additional test cases from a file
    for name, planned, actual in parse_cases(path):
        print(name)
        print(f" planned = [{', '.join(planned)}]")
        print(f" actual = [{', '.join(actual)}]")
        try:
            print_result(get_total_inversions(planned, actual))
        except ValueError as e:
            print(f" Error: {e}")
        print()

def run_large_check():

    # Reversed order of n deliveries has n(n - 1) / 2 inversions
    n = 100000
    planned = list(range(1, n + 1))
    actual = planned[::-1]
    print(f"Large check (n = {n})")
    print_result(get_total_inversions(planned, actual))
    print(f" Expected: {n * (n - 1) // 2}")


def print_result(inversions):
    print(f" Inversions: {inversions}")


if __name__ == "__main__":

    # Runs all required and additional test cases
    run_req_cases("./data/test_cases_2b.txt")

    # Runs the large count check
    run_large_check()