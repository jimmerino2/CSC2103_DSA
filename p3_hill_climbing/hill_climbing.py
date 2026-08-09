"""
CSC2103 Data Structures and Algorithms - Group Project
Problem 3: Hill Climbing for Optimisation (Heuristic Algorithm)

Scenario: Sunway University orientation walking route.
A student helper must lead a group of new students to every checkpoint on
campus and return to the starting point. The order of the checkpoints is free,
so the task is to find the visiting order with the shortest total walking
distance.
"""

import math
import random
from itertools import permutations

# Campus checkpoints and their (x, y) position in metres.
# The main entrance is treated as the origin (0, 0) and is always the start
# and end of the route.
CAMPUS_MAP = {
    "Main Entrance":       (0, 0),
    "Jeffrey Cheah Hall":  (95, 60),
    "North Building":      (150, 210),
    "South Building":      (60, 250),
    "University Library":  (230, 130),
    "Student Life Centre": (310, 245),
    "Sports Complex":      (390, 80),
    "Uni Residence":       (180, 380),
}

START = "Main Entrance"


def distance(point_a, point_b):
    """Straight line walking distance in metres between two checkpoints."""
    return math.hypot(point_a[0] - point_b[0], point_a[1] - point_b[1])


def route_distance(route, campus):
    """
    Objective function. Total distance of one full loop:
    start -> every checkpoint in order -> back to start.
    A lower value is a better solution.
    """
    total = 0.0
    for i in range(len(route) - 1):
        total += distance(campus[route[i]], campus[route[i + 1]])
    # add the walk back to the starting point to close the loop
    total += distance(campus[route[-1]], campus[route[0]])
    return total


def random_route(campus):
    """Generate a random starting solution with the start point fixed first."""
    stops = [name for name in campus if name != START]
    random.shuffle(stops)
    return [START] + stops


def get_neighbours(route):
    """
    Build the neighbourhood of a route.
    A neighbour is produced by swapping the position of any two checkpoints.
    Index 0 is skipped because the route must always begin at the main entrance.
    """
    neighbours = []
    for i in range(1, len(route)):
        for j in range(i + 1, len(route)):
            neighbour = route[:]
            neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
            neighbours.append(neighbour)
    return neighbours


def hill_climb(campus, start_route, show_steps=True):
    """
    Steepest ascent hill climbing.

    1. Start from a candidate route.
    2. Generate every neighbour of that route.
    3. Move to the best neighbour, but only if it is an improvement.
    4. Stop when no neighbour is better. That route is a local optimum.
    """
    current = start_route[:]
    current_cost = route_distance(current, campus)
    steps = 0

    if show_steps:
        print("Step 0 (starting route): %.2f m" % current_cost)

    while True:
        # 1. look at every neighbour of the current route
        neighbours = get_neighbours(current)

        # 2. find the neighbour with the lowest total distance
        best = min(neighbours, key=lambda r: route_distance(r, campus))
        best_cost = route_distance(best, campus)

        # 3. if no neighbour improves on the current route, we are at a
        #    local optimum and the search stops here
        if best_cost >= current_cost:
            break

        # 4. otherwise move to that neighbour and repeat
        current, current_cost = best, best_cost
        steps += 1
        if show_steps:
            print("Step %d: improved to %.2f m" % (steps, current_cost))

    if show_steps:
        print("No better neighbour found. Search stopped after %d step(s)." % steps)

    return current, current_cost, steps


def random_restart_hill_climb(campus, restarts, show_steps=False):
    """
    Run hill climbing several times from different random starting routes and
    keep the best result. This is the standard way of reducing the chance of
    being trapped in one poor local optimum.
    """
    best_route, best_cost = None, float("inf")
    for attempt in range(1, restarts + 1):
        route, cost, _ = hill_climb(campus, random_route(campus), show_steps)
        print("  Restart %2d -> %.2f m" % (attempt, cost))
        if cost < best_cost:
            best_route, best_cost = route, cost
    return best_route, best_cost


def brute_force_optimal(campus):
    """
    Check every possible route to find the true shortest one.
    Only used to verify the hill climbing result during testing. This is
    O(n!) and is not practical once the number of checkpoints grows.
    """
    stops = [name for name in campus if name != START]
    best_route, best_cost = None, float("inf")
    checked = 0
    for order in permutations(stops):
        route = [START] + list(order)
        cost = route_distance(route, campus)
        checked += 1
        if cost < best_cost:
            best_route, best_cost = route, cost
    return best_route, best_cost, checked


def print_route(title, route, cost):
    """Print a route in a readable form, wrapped to fit the console width."""
    stops = route + [route[0]]          # repeat the start to show a closed loop
    print("\n%s" % title)
    for i in range(0, len(stops), 3):
        line = " -> ".join(stops[i:i + 3])
        print("  " + line + (" ->" if i + 3 < len(stops) else ""))
    print("  Total walking distance: %.2f m" % cost)


def build_custom_map():
    """Let the user enter their own checkpoints instead of the sample data."""
    campus = {START: (0, 0)}
    count = int(input("Enter number of checkpoints (excluding the start point): "))
    for i in range(1, count + 1):
        print("\nCheckpoint %d:" % i)
        name = input("  Name: ")
        x = float(input("  X position in metres: "))
        y = float(input("  Y position in metres: "))
        campus[name] = (x, y)
    return campus


def main():
    print("=== Sunway University Orientation Walking Route ===")
    print("Hill Climbing for Optimisation\n")
    print("1. Use the sample campus map (8 checkpoints)")
    print("2. Enter my own checkpoints")
    choice = input("Select an option: ").strip()

    campus = CAMPUS_MAP if choice != "2" else build_custom_map()

    print("\nCheckpoints to visit:")
    for name, (x, y) in campus.items():
        print("  %-20s (%.0f, %.0f)" % (name, x, y))

    # the search starts from a random route, so a fixed seed is needed to make
    # a run repeatable and comparable against another
    seed = input("\nRandom seed (press Enter for 1): ").strip()
    random.seed(int(seed) if seed else 1)

    # --- single run of hill climbing ---
    start = random_route(campus)
    print_route("Randomly generated starting route:", start,
                route_distance(start, campus))

    print("\n=== Hill Climbing Search ===")
    final_route, final_cost, steps = hill_climb(campus, start)
    print_route("Best route found:", final_route, final_cost)

    start_cost = route_distance(start, campus)
    print("  Improvement over the starting route: %.2f m (%.1f%%)"
          % (start_cost - final_cost,
             (start_cost - final_cost) / start_cost * 100))

    # --- random restart version ---
    print("\n=== Random Restart Hill Climbing (10 restarts) ===")
    rr_route, rr_cost = random_restart_hill_climb(campus, 10)
    print_route("Best route across all restarts:", rr_route, rr_cost)

    # --- verification against the true optimum ---
    if len(campus) <= 9:
        print("\n=== Verification by Brute Force ===")
        opt_route, opt_cost, checked = brute_force_optimal(campus)
        print("  Routes checked: %d" % checked)
        print_route("True shortest route:", opt_route, opt_cost)
        print("\n  Single hill climb    : %.2f m  (%s)"
              % (final_cost, "optimal" if abs(final_cost - opt_cost) < 0.01
                 else "local optimum, %.2f m worse" % (final_cost - opt_cost)))
        print("  With random restarts : %.2f m  (%s)"
              % (rr_cost, "optimal" if abs(rr_cost - opt_cost) < 0.01
                 else "local optimum, %.2f m worse" % (rr_cost - opt_cost)))
    else:
        print("\nToo many checkpoints for brute force verification "
              "(%d! routes would need to be checked)." % (len(campus) - 1))


if __name__ == "__main__":
    main()
