import csv
import sys
import time

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    # Record current time
    start_time = time.perf_counter()

    path = shortest_path(source, target)

    # Print out elapsed time to execute shortes_path
    print_elapsed_time(start_time)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # handle "empty path" solution
    if source == target:
        # return empty list as per https://us.edstem.org/courses/176/discussion/23640
        return []

    # ------------ Node model ------------
    # Node.state = the person_id we have reached at this state
    # Node.action = the (movie_id, person_id) pair we followed from the parent state (person_id)
    # ------------------------------------

    # Initialize frontier to just the source person
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize an empty explored set
    explored = set()

    # Two counters used for optimisation analysis only
    nodes_created = 1
    nodes_explored = 0

    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            print("Nodes Created:", nodes_created)
            print("Nodes Explored:", nodes_explored)
            return None

        # Choose a node from the frontier
        node = frontier.remove()
        nodes_explored += 1

        # Mark node as explored
        explored.add(node.state)

        # Explore the node by examining it's neighbors and
        # adding them to the frontier if they do not link to the target person
        for movie_id, person_id in neighbors_for_person(node.state):

            # Optimisation:
            # check for a goal as neighbours identified before creating nodes and adding them to the frontier
            if person_id == target:
                print("Nodes Created:", nodes_created)
                print("Nodes Explored:", nodes_explored)
                actions = [ [movie_id,person_id] ]
                while node.parent is not None:
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                return actions

            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=[movie_id,person_id])
                nodes_created += 1
                frontier.add(child)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


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
