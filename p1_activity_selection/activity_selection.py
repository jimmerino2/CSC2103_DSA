def activity_selection(requests):
    # 1. Sort all requests by end time first 
    requests = sorted(requests, key=lambda x: x[2])

    # 2. Accept the first request, as it ends the earliest
    accepted = [requests[0]]
    rejected = []
    last_end = requests[0][2] # Get the end time of the last accepted request

    # 3. Loop through each following request
    for name, start, end in requests[1:]:
        if start >= last_end:
            # If the following request that ends the earliest starts AFTER the previous request's end time, accept it 
            accepted.append((name, start, end))
            last_end = end
        else:
            # If the following request that ends the earliest starts BEFORE the previous request's end time, reject it
            # This is because the request is overlapping with the previous time 
            rejected.append((name, start, end))

    # 4. Return list of accepted and rejected requests to be printed on console
    return accepted, rejected


def display_results(accepted, rejected):
    print("\n=== Scheduling Results ===")
    print("Accepted Bookings:")

    # 1. Print all accepted requests
    for name, start, end in accepted:
        print(f"  {name:<12} {start:04d} - {end:04d}")

    # 2. Print all rejected requests, if any
    print("\nRejected Bookings (overlap with an accepted slot):")
    if rejected:
        for name, start, end in rejected:
            print(f"  {name:<12} {start:04d} - {end:04d}")
    else:
        print("  None")

    print(f"\nTotal bookings scheduled: {len(accepted)} out of {len(accepted) + len(rejected)}")


if __name__ == '__main__':
    print("=== You are currently booking for Sunway Library - Training Room 01 ===")

    # 1. Ask how many groups to insert
    num_groups = int(input("Enter number of booking requests: "))

    # 2. Foreach group, input name, start time, and end time
    requests = []
    for i in range(1, num_groups + 1):
        print(f"\nRequest {i}:")
        name = input("  Group/Student name: ")
        start = int(input("  Start time (e.g. 0900): "))
        end = int(input("  End time (e.g. 1030): "))

        if end <= start:
            print("  Invalid: end time must be after start time. Skipping this entry.")
            continue

        requests.append((name, start, end))

    if not requests:
        print("\nNo valid booking requests entered. Exiting.")
    else:
        # 3. Use activity selection algorithm
        accepted, rejected = activity_selection(requests)

        # 4. Output maximum number and combinations
        display_results(accepted, rejected)