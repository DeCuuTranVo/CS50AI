import csv
import sys

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
    
    path = shortest_path(source, target)
    # print("path value:", path)

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
    
    # BREADTH FIRST SEARCH: EXHAUTIVE SEARCH + NEAREST NODE FIRST -> GUARANTEE TO FIND OPTIMAL CORECT SOLUTION 
    
    # Create path list
    shortest_path_list = []
    
    # # Traversed state list
    visited_state_list = []
    
    # Create a queue for nodes to be search
    queue_frontier = QueueFrontier()
    
    # Start with source node 
    source_node = Node(state=source, parent=None, action=None)
    
    # If source node is not destination node, add to the queue 
    if source_node.state == target:
        raise ValueError("Source and target actors are one person!")
    else:
        queue_frontier.add(source_node)
        visited_state_list.append(source_node.state)
    
    # While queue is not empty
    while (not queue_frontier.empty()):
        # Move the current node out of the queue 
        current_node = queue_frontier.remove()
        
        # Compute the edge go out of this node       
        # Get the list of nodes at the end of those edge
        neighbors = neighbors_for_person(current_node.state)
        
        # For each next edge and resulting state
        for item in neighbors:
            neighbor_edge_id = item[0]
            neighbor_node_id = item[1]
            # print(next_edge_id, next_node_id)
            
            if queue_frontier.contains_state(neighbor_node_id) or (neighbor_node_id == current_node.state) or (neighbor_node_id in visited_state_list): # Dont revisit the nodes already in the frontier, the parent node, or the already visited ones
                continue
            elif neighbor_node_id != target:  # If a new node is not the destination node,
                # Create a node 
                new_node = Node(state=neighbor_node_id, parent=current_node, action=neighbor_edge_id)
                # Add that node to the frontier queue
                queue_frontier.add(new_node)
                visited_state_list.append(new_node.state)
            else: #neighbor_node_id == target: # If a new nodes is the destination node,
                # Create that node
                target_node = Node(state= neighbor_node_id, parent=current_node, action=neighbor_edge_id)
                
                # Add that node to the frontiers and record in visited node
                queue_frontier.add(target_node)
                visited_state_list.append(target_node.state)
                
                # Backtracking the path
                backtrack_node = target_node
                while backtrack_node.parent != None: # when the parent node still exists
                    # print backtrack_node
                    # print(backtrack_node.state, backtrack_node.parent, backtrack_node.action)
                    
                    # Record the back track node to return path                    
                    path_item = (backtrack_node.action, backtrack_node.state)
                    # shortest_path_list.append(path_item)
                    shortest_path_list.insert(0, path_item)
                    
                    # Traverse to parent node
                    backtrack_node = backtrack_node.parent
                    
                # print("This line work")
                # print("shortest_path_list:", shortest_path_list)
                return shortest_path_list #Need to reverse due to the backtracking nature
            
    # print("This line dont")
    # If the algorithm can not find the target node (the path list is null or empty)
    # Return null
    assert len(shortest_path_list) == 0
    return None
    # print("shortest_path completed")


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


if __name__ == "__main__":
    main()
