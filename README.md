# CS-601: Pioneer Delivery Company’s Algorithm Portfolio

## Overview

This project is Part I (Greedy Algorithms) of the Pioneer Delivery Algorithm Portfolio.

**Programming language:** Python 3.13.

**Submitted files:**
- Source code: `task_1a.py`, `task_1b.py`, `task_1c.py`
- Data files: `data/deliveries.txt` (sample data), `data/test_cases_1a.txt`, `data/test_cases_1b.txt`, `data/test_cases_1c.txt`
- `README.md`

**Compiling and running:** From the project's root folder, run:

```
python3 task_1a.py
python3 task_1b.py
python3 task_1c.py
```

Each program runs its algorithm on `./data/deliveries.txt` first. Then, it runs its six required test cases from its own test file.

**Input-file format:** Each line of a delivery file is `id start finish`, separated by spaces. Times are integers, and blank lines are ignored. The test data file `data/deliveries.txt` contains:

```
D01 10 13
D02 2 5
D03 4 7
D04 1 8
D05 8 11
D06 11 14
D07 13 16
```

**Test-case file format:** Each test case begins with a `# Test N` line, followed by that case's delivery lines. A test with no delivery lines is the "no deliveries" case. For example:

```
# Test 1

# Test 2
D1 1 3
```

**Program organization:**

```
task_1a.py              Task A: maximum deliveries for one driver
task_1b.py              Task B: minimum number of drivers
task_1c.py              Task C: minimum deliveries rejected
data/deliveries.txt     Sample data (the 7-delivery example)
data/test_cases_1a.txt  Required test cases for Task A
data/test_cases_1b.txt  Required test cases for Task B
data/test_cases_1c.txt  Required test cases for Task C
```

Each task file has the same layout:
- `parse_data(path)` reads a delivery file.
- `parse_cases(path)` reads a test-case file.
- `sort(deliveries)` and `merge(left, right)` make up a merge sort (by finish time in Tasks A and C, and by start time in Task B).
- The main algorithm function is `max_deliveries` (A), `min_drivers` (B), or `min_rejected` (C).
- `run_req_cases(path)` runs the required test cases from a file.
- `print_result(...)` prints the output.

## Part 1A: Maximum Deliveries for One Driver

This implementation is in `task_1a.py`. It reads delivery data from `./data/deliveries.txt` and the six required test cases from `./data/test_cases_1a.txt`. It sorts the deliveries by earliest finish time with merge sort. Then, it optimally selects deliveries that do not conflict with other deliveries. After each run, it prints the selected delivery IDs, their start and finish times, and the total number of deliveries completed.

**1. What is the greedy choice made by your algorithm?**

The algorithm will always select the first delivery with the earliest finish time that does not conflict with any of the previously selected deliveries. This is achieved by sorting by finish time, where the algorithm will then choose deliveries whose start time is either at or after the finish time of the last selected delivery (`start >= latest_finish`).

**2. Why does this greedy strategy produce an optimal solution?**

By selecting the delivery that finishes the earliest, this leaves the most time remaining for later deliveries. Since any other choice would finish at the same time or later, this choice would leave the same number of deliveries, or more, still unavailable due to time conflicts.

For example, suppose there is some best possible schedule that did not start with the earliest-finishing delivery (e.g., it started with the 2nd earliest-finishing delivery). We could replace its first delivery with the earliest-finishing one. Since the earliest-finishing delivery cannot finish any later than the original first delivery, it still fits with the rest of the schedule. As such, the total number of deliveries stays the same. Thus, choosing the earliest-finishing delivery never makes the result worse.

This same reasoning can be applied to each later greedy choice with deliveries that start after the previous one finishes. Since this greedy choice cannot reduce the number of deliveries that can be completed, the final schedule is guaranteed to be as large as possible.

**3. What is the running time of your algorithm?**

The running time is O(n log n):
- Parsing the input file: O(n)
- Merge sort by finish time: O(n log n)
- One pass to select compatible deliveries: O(n)

Merge sort is the dominant term, so the overall running time is O(n log n).

## Part 1B: Minimum Number of Drivers

This implementation is in `task_1b.py`. It reads delivery data from `./data/deliveries.txt` and the six required test cases from `./data/test_cases_1b.txt`. It sorts the deliveries by earliest start time with merge sort, then assigns each delivery to a driver using a min-heap (priority queue). After each run, it prints each driver's schedule and the minimum number of drivers required.

**1. What information is stored in the priority queue?**

The priority queue stores one entry per driver. Each entry is a pair with the data `(finish time, driver ID)`, with `finish time` being the finish time of the most recent delivery for the driver while `driver ID` is the driver's index. The heap is ordered by finish time, so the driver who becomes available the soonest is always found at the front of the priority queue.

**2. How is a driver selected for each new delivery?**

Deliveries are processed in order of start time. For each delivery, the algorithm checks the driver at the top of the heap (since this driver becomes available the earliest). If that driver's finish time is at or before the new delivery's start time (`finish <= start`), that driver takes the delivery. Otherwise, every driver is still busy, so a new driver is added. After the assignment, the driver is put back into the heap with their new finish time.

**3. Why does this algorithm use the minimum possible number of drivers?**

This algorithm uses the minimum possible number of drivers as new drivers are only added when a delivery starts and every existing driver is currently occupied. If all of the existing drivers are in the middle of a delivery and the new delivery is unable to be handled, that would mean that there are more deliveries happening simultaneously than there are drivers. Since overlapping deliveries cannot share a driver, there must be a number of drivers equivalent to the number of deliveries needed at that moment. Since the algorithm never adds a driver unless this occurs, it never uses more drivers than the largest number of deliveries running at the same time. Thus, this algorithm uses the fewest possible drivers.

**4. What is the running time?**

The running time is O(n log n):
- Parsing the input file: O(n)
- Merge sort by start time: O(n log n)
- There are n deliveries, where each delivery has one heap removal and one heap insertion that each take O(log n): O(n log n)

The sort and the heap operations are O(n log n), so the overall running time is O(n log n).

## Part 1C: Interview-Style Variant

This implementation is in `task_1c.py`. It reads delivery data from `./data/deliveries.txt` and the six required test cases from `./data/test_cases_1c.txt`. It uses the same merge sort and greedy selection as Task A to find the largest set of compatible deliveries. Then, the algorithm subtracts that number from the total number of deliveries. After each run, it prints the minimum number of deliveries that must be rejected.

**1. How is this problem related to Task A?**

This problem is related to Task A in that all deliveries that remain after rejecting some deliveries must all be compatible with each other. The most deliveries that can remain is the same amount of compatible deliveries produced in Task A's algorithm. Thus, rejecting as few deliveries as possible is the same problem as keeping as many deliveries as possible, so Task A's algorithm solves it.

**2. If the maximum number of compatible deliveries is k, how many deliveries must be rejected?**

If there are `n` total deliveries and `k` is the maximum number of compatible deliveries, then `n - k` deliveries must be rejected.

**3. What is the running time of your algorithm?**

The running time is O(n log n):
- Parsing the input file: O(n)
- Merge sort by finish time: O(n log n)
- One pass to count compatible deliveries: O(n)
- Subtracting `k` from `n`: O(1)

Merge sort is the dominant term, so the overall running time is O(n log n).

## Part 1D: When a Greedy Choice Fails

**1. Deliveries Table**

| Delivery | Ready time Rj | Profit Pj |
|----------|---------------|-----------|
| D1 | 0 | 20 |
| D2 | 0 | 15 |
| D3 | 1 | 10 |

**2. Schedule produced by greedy strategy G**

G prioritizes the deliveries in order of decreasing profit (D1, D2, D3). This means it places each delivery in the earliest open slot at or after its ready time.

- Place D1 (ready time of 0) in slot 0. Delay = 0, so V1 = 20 / (1 + 0) = 20.
- Place D2 (ready time of 0) in slot 1. Delay = 1, so V2 = 15 / (1 + 1) = 7.5.
- Place D3 (ready time of 1) in slot 2. Delay = 1, so V3 = 10 / (1 + 1) = 5.

**V(G) = 20 + 7.5 + 5 = 32.5**

**3. A better schedule S**

Let's keep D1 in slot 0, then swap slot 1 to D3 and D2 to slot 2.

- Place D1 in slot 0. Delay = 0, so V1 = 20 / (1 + 0) = 20.
- Place D3 in slot 1. Delay = 0, so V3 = 10 / (1 + 0) = 10.
- Place D2 in slot 2. Delay = 2, so V2 = 15 / (1 + 2) = 5.

**V(S) = 20 + 10 + 5 = 35**

**4. Why this proves G is not always optimal**

Since V(S) = 35 is greater than V(G) = 32.5, this means that there exists a better schedule than the one that G produces. Since an optimal strategy can never be beaten by another strategy, this means that G is not always optimal.

## Test Results

In the test files, delivery IDs are assigned in the order the intervals are listed (D1, D2, ...). Selected deliveries are listed in the order the algorithm chose them. In Tasks A and B, more than one optimal answer can exist. Thus, the results below are the schedules the programs produced.

### Task A: Maximum Deliveries for One Driver

| Test | Delivery Intervals | Selected (ID: start-finish) | Total | Expected |
|------|--------------------|-----------------------------|-------|----------|
| 1 | No deliveries | None | 0 | 0 |
| 2 | (1, 3) | D1: 1-3 | 1 | 1 |
| 3 | (1, 3), (3, 5), (5, 7) | D1: 1-3, D2: 3-5, D3: 5-7 | 3 | 3 |
| 4 | (1, 5), (2, 6), (3, 7) | D1: 1-5 | 1 | 1 |
| 5 | (5, 7), (1, 3), (3, 5), (2, 4) | D2: 1-3, D3: 3-5, D1: 5-7 | 3 | 3 |
| 6 | (1, 4), (2, 4), (4, 6) | D1: 1-4, D3: 4-6 | 2 | 2 |

Sample data (`deliveries.txt`): D02: 2-5, D05: 8-11, D06: 11-14, total deliveries: 3.

### Task B: Minimum Number of Drivers

| Test | Delivery Intervals | Driver Schedules | Drivers | Expected |
|------|--------------------|------------------|---------|----------|
| 1 | No deliveries | None | 0 | 0 |
| 2 | (1, 3) | Driver 1: D1 | 1 | 1 |
| 3 | (1, 3), (3, 5), (5, 7) | Driver 1: D1 D2 D3 | 1 | 1 |
| 4 | (1, 5), (2, 6), (3, 7) | Driver 1: D1; Driver 2: D2; Driver 3: D3 | 3 | 3 |
| 5 | (1, 4), (2, 5), (4, 7), (5, 8) | Driver 1: D1 D3; Driver 2: D2 D4 | 2 | 2 |
| 6 | (5, 8), (1, 4), (2, 5), (4, 6), (6, 9) | Driver 1: D2 D4 D5; Driver 2: D3 D1 | 2 | 2 |

Sample data (`deliveries.txt`): Driver 1: D04 D06; Driver 2: D02 D05 D07; Driver 3: D03 D01, total drivers: 3.

### Task C: Minimum Deliveries Rejected

| Test | Delivery Intervals | Rejected | Expected |
|------|--------------------|----------|----------|
| 1 | No deliveries | 0 | 0 |
| 2 | (1, 3) | 0 | 0 |
| 3 | (1, 3), (3, 5), (5, 7) | 0 | 0 |
| 4 | (1, 5), (2, 6), (3, 7) | 2 | 2 |
| 5 | (5, 7), (1, 3), (3, 5), (2, 4) | 1 | 1 |
| 6 | (1, 2), (2, 3), (3, 4), (1, 3) | 1 | 1 |

Sample data (`deliveries.txt`): 4 deliveries rejected (3 of the 7 can be kept).
