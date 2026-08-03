# Activity Selection Algorithm - Sunway Library Training Room Booking System

## Overview

Given that many students want to book Training Room 01 in Sunway University Library at different time slots, the **Activity Selection Algorithm** decides on how to schedule the maximum number of student meetings in the room throughout the day without any overlap.

## Problem Description

Given a list of booking requests, each with a group name or student's name, start time and end time, the goal is to select the largest possible subset of requests such that no two selected bookings overlap.

## How the Algorithm Works

1. **Sort** all booking requests by their **end time**.
2. **Select** the first request in the sorted list (it finishes soonest, leaving the most time for others).
3. **Scan** through the remaining requests in order:
   - If a request's **start time** is at or after the **end time** of the last accepted booking, it is **accepted**.
   - Otherwise, it is **rejected** (it overlaps with an already-accepted booking).
4. Repeat until all requests have been checked.
5. Output accepted and rejected requests, as well as the total number of accepted requests

Since decision-making is always optimal at every stage, there is no need to backtrack or reconsider previous options, resulting in the maximum possible number of scheduled meetings.

**Time Complexity:** O(n log n) for sorting records by their end time, O(n) for selecting and processing each sorted record.

## Requirements

- Python 3.x (no external libraries required)

## How to Run

```bash
python3 activity_selection.py
```

## Usage

1. Enter the number of booking requests when prompted.
2. For each request, enter:
   - Group/Student name
   - Start time (24-hour format, e.g. `0900`)
   - End time (24-hour format, e.g. `1030`)
3. The program will display:
   - **Accepted Bookings** — the maximum non-overlapping schedule
   - **Rejected Bookings** — requests that conflicted with an accepted booking
   - **Total bookings scheduled**

### Example

**Input:**

```
Enter number of booking requests: 5

Request 1:
  Group/Student name: Group A
  Start time (24hr, e.g. 0900): 0900
  End time (24hr, e.g. 1030): 1030

Request 2:
  Group/Student name: Group B
  Start time (24hr, e.g. 0900): 0930
  End time (24hr, e.g. 1030): 1100

Request 3:
  Group/Student name: Group C
  Start time (24hr, e.g. 0900): 1030
  End time (24hr, e.g. 1030): 1130

Request 4:
  Group/Student name: Group D
  Start time (24hr, e.g. 0900): 1100
  End time (24hr, e.g. 1030): 1300

Request 5:
  Group/Student name: Group E
  Start time (24hr, e.g. 0900): 1130
  End time (24hr, e.g. 1030): 1230
```

**Output:**

```
=== Scheduling Results ===
Accepted Bookings:
  Group A      0900 - 1030
  Group C      1030 - 1130
  Group E      1130 - 1230

Rejected Bookings (overlap with an accepted slot):
  Group B      0930 - 1100
  Group D      1100 - 1300

Total bookings scheduled: 3 out of 5
```

## Input Validation

- End time must be later than start time; invalid entries are skipped with a warning.
- Times should be entered as 4-digit 24-hour values (e.g. `0900`, `1345`).

## Strengths

- Guarantees the mathematically **maximum number** of non-overlapping bookings (provably optimal, not an approximation).
- Efficient: O(n log n) time complexity.
- Simple, predictable logic with no backtracking required.

## Limitations

- Optimizes only for the **count** of bookings, not total room utilization time, urgency, or fairness — a single long meeting may be rejected in favor of several shorter ones.
- Treats all requests as equally important; does not account for priority, group size, or booking urgency.
- Assumes all requests are known upfront; does not support dynamic/real-time booking requests or cancellations.

## File Structure

```
.
├── activity_selection.py   # Main program
└── README.md                # This file
```
