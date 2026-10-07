# CS-601: Pioneer Delivery Company’s Algorithm Portfolio


## Part 1A: Maximum Deliveries for One Driver

This implementation is in `task_1a.py`. It reads delivery data from `./data/deliveries.txt` and the six required test cases from `./data/test_cases_1a.txt`. It sorts the deliveries by earliest finish time with merge sort. Then, it optimally selects deliveries that do not conflict with other deliveries. After each run, it prints the selected delivery IDs, their start and finish times, and the total number of deliveries completed.

**1. What is the greedy choice made by your algorithm?**

The algorithm will always select the first delivery with the earliest finish time that does not conflict with any of the previously selected deliveries. This is achieved by sorting by finish time, where the algorithm will then choose deliveries whose start time is either at or after the finish time of the last selected delivery (`start >= latest_finish`).

**2. Why does this greedy strategy produce an optimal solution?**

By selecting the delivery that finishes the earliest, this leaves the most time remaining for later deliveries. Since any other choice would finish at the same time or later, this choice would leave the same number of deliveries, or more, still unavailable due to time conflicts.

For example, suppose there is some best possible schedule did not start with the earliest-finishing delivery (e.g., it started with the 2nd earliest-finishing delivery). We could replace its first delivery with the earliest-finishing one. Since the earliest-finishing delivery cannot finish any later than the original first delivery, it still fits with the rest of the schedule. As such, the total number of deliveries stays the same. Thus, choosing the earliest-finishing delivery never makes the result worse.

This same reasoning can be applied to each later greedy choice with deliveries that start after the previous one finishes. Since this greedy choice cannot reduce the number of deliveries that can be completed, the final schedule is guaranteed to be as large as possible.

**3. What is the running time of your algorithm?**

The running time is O(n log n):
- Parsing the input file: O(n)
- Merge sort by finish time: O(n log n)
- One pass to select compatible deliveries: O(n)

Merge sort is the dominant term, so the overall running time is O(n log n).