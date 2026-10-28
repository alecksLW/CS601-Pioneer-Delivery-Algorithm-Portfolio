# CS-601: Pioneer Delivery Company’s Algorithm Portfolio

## Overview

This project is Part II (Divide and Conquer) of the Pioneer Delivery Algorithm Portfolio. It does not reuse any code from Part I.

**Programming language:** Python 3.13.

**Dependencies:** None.

**Submitted files:**
- Source code: `task_2a.py`, `task_2b.py`, `task_2c.py`, `task_2d.py`
- Data files: `data/test_cases_2a.txt`, `data/test_cases_2b.txt`, `data/test_cases_2c.txt`
- `README.md`

**Compiling and running:** From the project's part2 folder, run:

```
python3 task_2a.py
python3 task_2b.py
python3 task_2c.py
python3 task_2d.py
```

Each of the first three programs runs its algorithm on every case in its own test file. `task_2d.py` runs the correctness checks and timings for Task D.

**Test-case file format:** Each test case begins with a `# Test ...` line, followed by that case's input. The input lines depend on the task.

Task A (`data/test_cases_2a.txt`) lists one location per line as `id x y`:

```
# Test A1
A 0 0
B 3 4
```

Task B (`data/test_cases_2b.txt`) has a `planned:` line and an `actual:` line, each listing the delivery IDs in order:

```
# Test B1
planned: A B C D E
actual: A C D B E
```

Task C (`data/test_cases_2c.txt`) has a `T:` line with the delivery times and a `k:` line with the rank (1-based):

```
# Test C1
T: 18 4 29 11 4 16 35 9 22
k: 5
```

Tests named A1-A4, B1-B4, and C1-C5 are the required cases. Tests named E1, E2, and so on are my own additional edge cases.

**Program organization:**

```
task_2a.py              Task A: closest delivery locations
task_2b.py              Task B: counting dispatch-order inversions
task_2c.py              Task C: selecting a delivery-time threshold
task_2d.py              Task D: reference checks and timings
data/test_cases_2a.txt  Required and additional test cases for Task A
data/test_cases_2b.txt  Required and additional test cases for Task B
data/test_cases_2c.txt  Required and additional test cases for Task C
```

Each task file (A, B, and C) has the same layout:
- `parse_cases(path)` reads a test-case file.
- The main algorithm function is `closest_pair` (A), `get_total_inversions` (B), or `get_kth_smallest` (C).
- `run_req_cases(path)` runs all of the test cases from a file.
- `print_result(...)` prints the output.

## Part 2A: Closest Delivery Locations

This implementation is in `task_2a.py`. It reads the locations for each test case from `./data/test_cases_2a.txt`. It sorts the points by x with merge sort once, then recursively splits them at the middle index into a left half and a right half, and checks the strip around the dividing line when combining the halves. The y-sorted order is merged during the recursion and is not sorted again. After each case, it prints the IDs of the closest pair, their squared distance, and the actual distance. If there are fewer than two locations, it prints a clear error message.

## Part 2B: Counting Dispatch-Order Inversions

This implementation is in `task_2b.py`. It reads the planned and actual orders for each test case from `./data/test_cases_2b.txt`. It rewrites the actual order as planned-order ranks, then counts the inversions with a merge sort that counts the cross-half inversions while merging. After each case, it prints the planned order, the actual order, and the total number of inversions. It also runs a large-count check, where the actual order is the reverse of a planned order of 100,000 deliveries. If the two orders are empty, have different delivery IDs, or repeat a delivery ID, it prints a clear error message.

## Part 2C: Selecting a Delivery-Time Threshold

This implementation is in `task_2c.py`. It reads the delivery times and `k` for each test case from `./data/test_cases_2c.txt`. It uses the median-of-medians algorithm with groups of at most 5 to choose a pivot, partitions the times into values less than, equal to, and greater than the pivot, and recurses only into the partition that holds rank `k`. After each case, it prints the delivery times, `k`, and the k-th smallest value. If the list is empty, a time is negative, or `k` is not between 1 and n, it prints a clear error message.

## Part 2D: Validation and Algorithm Analysis

`task_2d.py` compares each algorithm with a simple reference solution on small random inputs (brute force for Task A, two nested loops for Task B, and sorting for Task C), then times each algorithm on three increasing input sizes. The timings are machine-dependent, so they will differ slightly from run to run.

## Test Results

In Task A, if more than one closest pair exists, any one of them is acceptable. In Tasks B and C, the cases that are invalid inputs print a clear error message instead of a result.

### Task A: Closest Delivery Locations

| Test | Input Locations (id, x, y) | Closest Pair | Squared Distance | Expected |
|------|----------------------------|--------------|------------------|----------|
| A1 | A(0, 0), B(3, 4) | A, B | 25 | A, B; 25 |
| A2 | A(0, 0), B(7, 2), C(4, 5), D(5, 5), E(12, 2), F(2, 9) | C, D | 1 | C, D; 1 |
| A3 | A(-3, 1), B(-3, 11), C(1, 1), D(2, 15) | A, C | 16 | A, C; 16 |
| A4 | A(-5, -5), B(-5, -2), C(6, 8) | A, B | 9 | A, B; 9 |
| E1 | A(0, 0), B(1, 0), C(10, 10), D(10, 11) (two tied pairs) | A, B | 1 | A, B or C, D; 1 |
| E2 | A(5, 0), B(5, 10), C(5, 3), D(5, 20), E(5, 12) (same x) | B, E | 4 | B, E; 4 |

### Task B: Counting Dispatch-Order Inversions

| Test | Planned Order | Actual Order | Inversions | Expected |
|------|---------------|--------------|------------|----------|
| B1 | [A, B, C, D, E] | [A, C, D, B, E] | 2 | 2 |
| B2 | [A, B, C, D] | [A, B, C, D] | 0 | 0 |
| B3 | [A, B, C, D] | [D, C, B, A] | 6 | 6 |
| B4 | [A] | [A] | 0 | 0 |
| E1 | [A, B, C, D, E] | [A, B, D, C, E] | 1 | 1 |
| E2 | [A, B, C] | [A, B, D] | Error (different delivery IDs) | Error |
| E3 | [A, B, C] | [A, B, B] | Error (repeated delivery ID) | Error |

Large-count check (n = 100,000, reversed order): 4,999,950,000 inversions, which matches the expected n(n - 1) / 2.

### Task C: Selecting a Delivery-Time Threshold

| Test | Delivery Times T | k | Result | Expected |
|------|------------------|---|--------|----------|
| C1 | [18, 4, 29, 11, 4, 16, 35, 9, 22] | 5 | 16 | 16 |
| C2 | [18, 4, 29, 11, 4, 16, 35, 9, 22] | 2 | 4 | 4 |
| C3 | [18, 4, 29, 11, 4, 16, 35, 9, 22] | 9 | 35 | 35 |
| C4 | [7, 7, 7, 7, 7, 7] | 4 | 7 | 7 |
| C5 | [8, 3] | 1 | 3 | 3 |
| E1 | [1, 2, ..., 20] (already sorted) | 10 | 10 | 10 |
| E2 | [20, 19, ..., 1] (reverse-sorted) | 15 | 15 | 15 |
| E3 | 30 values with many duplicates (1, 2, 3, 4, 5, 15) | 20 | 3 | 3 |
| E4 | [1, 2, 3] | 4 | Error (k out of range) | Error |
| E5 | [] (no delivery times) | 1 | Error (no delivery times) | Error |