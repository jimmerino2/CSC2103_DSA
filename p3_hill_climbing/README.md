# Hill Climbing Algorithm - Sunway Campus Orientation Walking Route

## Overview
During orientation, a student helper must lead a group of new students to every checkpoint on the Sunway University campus and return to the starting point. Since the order of the checkpoints is free, the **Hill Climbing Algorithm** searches for the visiting order that gives the shortest total walking distance, without having to examine every possible route.

## Problem Description
Given a set of campus checkpoints and their positions, with the main entrance fixed as both the start and the end of the loop, the goal is to find the visiting order with the **minimum total walking distance**. This is a Travelling Salesman Problem: the number of possible routes grows as (n-1)!, so checking all of them stops being practical very quickly. Hill climbing is a heuristic that finds a good route fast, without any guarantee that it is the best one.

## How the Algorithm Works
1. **Start** from a randomly generated route that begins at the main entrance.
2. **Measure** the current route using the objective function — the total distance of the closed loop, where a lower value is better.
3. **Generate the neighbourhood**: every route that can be reached by swapping the position of any two checkpoints. For n checkpoints this gives O(n²) neighbours.
4. **Pick the best neighbour**, that is, the one with the lowest total distance.
5. **Move to it only if it improves** on the current route:
   - If it is shorter, accept it and repeat from step 3.
   - If no neighbour is shorter, **stop**. The current route is a **local optimum**.
6. Output the route found, the distance, and the improvement over the starting route.

Because the algorithm only ever accepts an improving move, it is fast and simple, but it can finish at a route that is better than everything nearby yet still worse than the true best route. To reduce this, the program also runs **random restart hill climbing**: ten independent climbs from ten different random starting routes, keeping the best result of the ten.

The program then verifies the result by **brute force**, checking all 5,040 possible routes for the 8-checkpoint sample map. Brute force is used here only as a measuring stick, so the quality of the heuristic can be shown rather than assumed. It is O(n!) and is skipped automatically for larger maps.

**Time Complexity:** O(k × n³) for hill climbing, where k is the number of improving steps taken — each step builds O(n²) neighbours and evaluates each one in O(n). Brute force verification is O(n!).
**Space Complexity:** O(n²) to hold the neighbourhood of the current route.

## Requirements
- Python 3.x (no external libraries required)

## How to Run

```bash
python3 hill_climbing.py
```

## Usage
1. Choose the map when prompted:
   - Option `1` uses the built-in sample campus map of 8 checkpoints.
   - Option `2` lets you enter your own checkpoints, each with a name and an (x, y) position in metres.
2. Enter a random seed, or press Enter to use seed 1. The seed is fixed so that any run can be reproduced exactly.
3. The program will display:
   - **Randomly generated starting route** — where the search begins
   - **Hill Climbing Search** — every improving step, and the route the search stops at
   - **Random Restart Hill Climbing** — the result of all 10 restarts and the best of them
   - **Verification by Brute Force** — the true shortest route, and whether the heuristic found it

### Example

**Input:**

```
1. Use the sample campus map (8 checkpoints)
2. Enter my own checkpoints
Select an option: 1

Random seed (press Enter for 1): 1
```

**Output:**

```
Randomly generated starting route:
  Main Entrance -> University Library -> Uni Residence ->
  Sports Complex -> South Building -> Jeffrey Cheah Hall ->
  Student Life Centre -> North Building -> Main Entrance
  Total walking distance: 2155.25 m

=== Hill Climbing Search ===
Step 0 (starting route): 2155.25 m
Step 1: improved to 1825.40 m
Step 2: improved to 1640.76 m
Step 3: improved to 1466.78 m
Step 4: improved to 1385.86 m
Step 5: improved to 1331.06 m
No better neighbour found. Search stopped after 5 step(s).

Best route found:
  Main Entrance -> South Building -> North Building ->
  Uni Residence -> Student Life Centre -> Sports Complex ->
  University Library -> Jeffrey Cheah Hall -> Main Entrance
  Total walking distance: 1331.06 m
  Improvement over the starting route: 824.18 m (38.2%)

=== Verification by Brute Force ===
  Routes checked: 5040

  Single hill climb    : 1331.06 m  (optimal)
  With random restarts : 1331.06 m  (optimal)
```

Seed 1 reaches the true optimum in five moves. Seed 4 does not, and is the more useful demonstration:

```
  Single hill climb    : 1421.88 m  (local optimum, 90.82 m worse)
  With random restarts : 1331.06 m  (optimal)
```

The single climb stops 90.82 m short because **no single swap improves that route** — every neighbour is worse, even though a shorter route exists further away. Random restart escapes it, because at least one of the ten starting points leads to the optimum.

## Input Validation
- The seed field accepts an empty entry and falls back to seed 1.
- Brute force verification runs only for maps of 9 checkpoints or fewer; above that the program reports how many routes would need to be checked instead of attempting it.
- The main entrance is always fixed at index 0 and is never swapped, so every generated route remains a valid closed loop.

## Strengths
- Fast: reaches a good route in a handful of steps instead of examining all (n-1)! routes.
- Simple to implement and easy to trace, since every step either improves the route or ends the search.
- Scales to problem sizes where exhaustive search is impossible.
- Random restart substantially raises the chance of finding the true optimum at a very small cost.

## Limitations
- **No guarantee of optimality.** The result is a local optimum, which may or may not be the global one, as seed 4 demonstrates.
- Never accepts a worse move, so it cannot climb out of a local optimum on its own — restarting is what rescues it, not the algorithm itself.
- The outcome depends on the random starting route, so different seeds give different answers.
- The neighbourhood definition limits what the search can reach; a swap-based neighbourhood cannot make certain rearrangements in one move.

## File Structure

```
.
├── hill_climbing.py   # Main program
└── README.md          # This file
```
