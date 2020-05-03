import csv
import sys
import time

from degrees import load_data, shortest_path, people, movies


def main():
    """
    Test harness to exercise the degrees.py project via the 'small' dataset.
    """

    test_cases = [

        # Connected
        {'source': '102',    'target': '102',    'expected': 0},   # Kevin Bacon > Kevin Bacon
        {'source': '914612', 'target': '914612', 'expected': 0},   # Emma Watson > Emma Watson
        {'source': '102',    'target': '158',    'expected': 1},   # Kevin Bacon > Tom Hanks
        {'source': '158',    'target': '102',    'expected': 1},   # Tom Hanks > Kevin Bacon
        {'source': '102',    'target': '193',    'expected': 1},   # Kevin Bacon > Demi Moore
        {'source': '193',    'target': '102',    'expected': 1},   # Demi Moore > Kevin Bacon
        {'source': '1597',   'target': '398',    'expected': 2},   # Mandy Patinkin > Sally Field
        {'source': '398',    'target': '1597',   'expected': 2},   # Sally Field > Mandy Patinkin
        {'source': '163',    'target': '705',    'expected': 4},   # Dustin Hoffman > Robin Wright
        {'source': '705',    'target': '163',    'expected': 4},   # Robin Wright > Dustin Hoffman
        {'source': '163',    'target': '1697',   'expected': 5},   # Dustin Hoffman > Chris Sarandon
        {'source': '1697',   'target': '163',    'expected': 5},   # Chris Sarandon > Dustin Hoffman

        # Not Connected
        {'source': '914612', 'target': '102',    'expected': -1},  # Emma Watson > Kevin Bacon
        {'source': '102',    'target': '914612', 'expected': -1},  # Kevin Bacon > Emma Watson
        {'source': '914612', 'target': '158',    'expected': -1},  # Emma Watson > Tom Hanks
        {'source': '158',    'target': '914612', 'expected': -1}   # Tom Hanks > Emma Watson
    ]

    # Load data from files into memory
    print("Loading 'small' data...")
    load_data("small")
    print("Data loaded.")

    for test_case in test_cases:

        source = test_case['source']
        target = test_case['target']

        print("--------------------------------------------------")
        print(f"{people[source]['name']} > {people[target]['name']}")

        # Record current time
        start_time = time.perf_counter()

        path = shortest_path(source, target)

        # Print out elapsed time to execute shortes_path
        print_elapsed_time(start_time)

        if path is None:
            degrees = -1
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")

        print(f"Degrees of Separation: Expected: {test_case['expected']} Calculated: {degrees}")

        if degrees == test_case['expected']:
            print("TEST CASE PASSED")
        else:
            print("TEST CASE FAILURE!")
            exit()

    print("--------------------------------------------------")
    print("ALL TEST CASES PASSED")


def print_elapsed_time(start_time):
    """
    Prints a pretty version of the elapsed time from start_time to now
    """
    elapsed_time = time.perf_counter() - start_time
    seconds = int(elapsed_time)
    minutes, seconds = divmod(seconds, 60)
    pretty_time = ""
    if minutes > 0:
        pretty_time = '%d mins %d secs' % (minutes, seconds)
    else:
        pretty_time = f"{elapsed_time:0.2f} secs"
    print("Elapsed time:", pretty_time)


if __name__ == "__main__":
    main()
