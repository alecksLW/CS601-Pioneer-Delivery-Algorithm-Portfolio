# task_1b.py
# Task B: Minimum Number of Drivers

import heapq


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

    # Each test case begins with a '# Test N' line, followed by 'id start finish' lines
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

    # Sort by earliest start time using merge sort (O(nlog(n)))
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
        if left[i][1] <= right[j][1]:
            sorted.append(left[i])
            i += 1
        else:
            sorted.append(right[j])
            j += 1

    # Append the rest of the entries
    sorted.extend(left[i:])
    sorted.extend(right[j:])
    return sorted


def min_drivers(deliveries):

    # Deliveries scheduled for each driver
    schedules = []

    # Priority queue with the data (finish time, driver ID)
    queue = []

    for id, start, finish in sort(deliveries):

        # If a driver is not occupied, give them the delivery
        if queue and queue[0][0] <= start:
            _, driver = heapq.heappop(queue)
        else:
            # Add a new driver to handle the delivery
            driver = len(schedules)
            schedules.append([])

        # Add the respective delivery to the driver's schedule
        schedules[driver].append((id, start, finish))

        # Push the finish time and driver ID onto the min-heap
        heapq.heappush(queue, (finish, driver))
    return schedules


def run_req_cases(path):

    # Required test cases, read from a file
    for n, deliveries in enumerate(parse_cases(path), 1):
        print(f"Test #{n}")
        print_result(min_drivers(deliveries))
        print()


def print_result(schedules):
    for d, schedule in enumerate(schedules, 1):
        ids = " ".join(id for id, start, finish in schedule)
        print(f" Driver {d}: {ids}")
    print(f" Minimum drivers required: {len(schedules)}")


if __name__ == "__main__":

    # Runs the algorithm from a file
    print_result(min_drivers(parse_data("./data/deliveries.txt")))
    print()

    # Runs all required test cases
    run_req_cases("./data/test_cases_1b.txt")