# task_1a.py
# Task A: Maximum Deliveries for One Driver

def parse_data(path):
    
    # Each line is structured as 'id start finish'
    entries = []
    with open(path) as f:
        for line in f:
            parts = line.split()

            # Use the first three entries
            if len(parts) >= 3:
                entries.append((parts[0], int(parts[1]), int(parts[2])))
    return entries


def parse_cases(path):

    # Each test case begins with a '# Test XYZ' line, followed by line(s) of 'id start finish'
    cases = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                cases.append([])
                continue

            parts = line.split()
            if len(parts) >= 3:
                cases[-1].append((parts[0], int(parts[1]), int(parts[2])))
    return cases


def sort(deliveries):
    
    # Base case
    if len(deliveries) <= 1:
        return deliveries

    # Sort by earliest finish time using merge sort (O(nlog(n)))
    mid = len(deliveries) // 2
    left = sort(deliveries[:mid])
    right = sort(deliveries[mid:])
    return merge(left, right)
 
 
def merge(left, right):
    sorted = []
    i = 0
    j = 0

    # Keep sorting until one side is exhausted
    while i < len(left) and j < len(right):
        if left[i][2] <= right[j][2]:
            sorted.append(left[i])
            i += 1
        else:
            sorted.append(right[j])
            j += 1

    # Append the rest of the entries
    sorted.extend(left[i:])
    sorted.extend(right[j:])
    return sorted


def max_deliveries(deliveries):
    selected = []
    latest_finish = float("-inf")

    for id, start, finish in sort(deliveries):

        # Select a delivery with a non-conflicting start time
        if start >= latest_finish:
            selected.append((id, start, finish))

            # The selected delivery now has the latest finish time
            latest_finish = finish
    return selected


def run_req_cases(path):

    # Required test cases, read from a file
    for n, deliveries in enumerate(parse_cases(path), 1):
        print(f"Test #{n}")
        print_result(max_deliveries(deliveries))
        print()


def print_result(selected):
    for id, start, finish in selected:
        print(f" {id}: {start} - {finish}")
    print(f" Total deliveries completed: {len(selected)}")


if __name__ == "__main__":

    # Runs the algorithm from a file
    print_result(max_deliveries(parse_data("./data/deliveries.txt")))
    print()

    # Runs all required test cases
    run_req_cases("./data/test_cases_1a.txt")