import pygraphviz as pgv
from matrix_client.api import MatrixHttpApi

# Set the access token for the user
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# Create a Matrix HTTP API client
matrix = MatrixHttpApi("https://matrix.org", token=ACCESS_TOKEN)

def add_nodes_to_graph(parent_node, graph, visited_nodes):
    if parent_node in visited_nodes:
        return
    visited_nodes.add(parent_node)
    events = matrix.get_room_state(parent_node)
    space_event = next((event for event in events if event["type"] in ["m.space", "m.space.child"]), None)
    if space_event is not None:
        space = space_event["content"]
        child_rooms = [event["state_key"] for event in events if event["type"] in ["m.space.child", "m.space"]]
        if not child_rooms:
            print(f"No rooms or spaces found in {parent_node}")
            return
        print(f"Found {len(child_rooms)} rooms and spaces in {parent_node}: {child_rooms}")

        # Add the rooms and spaces to the graph
        for room_id in child_rooms:
            # Get information about the room or space
            try:
                room_name_dict = matrix.get_room_name(room_id)
                room_name = room_name_dict["name"]
            except:
                print(f"Error getting room name for {room_id}")
                continue
            if room_name is not None and "Core" not in room_name:
                if space_event["type"] == "m.space.child":
                    room_type = "room"
                else:
                    room_type = "space"
                graph.add_node(room_id, label=room_name)
                graph.add_edge(parent_node, room_id)
                print(f"Added {room_type} {room_id} to the graph with label {room_name}")

            # Add the child nodes to the graph
            add_nodes_to_graph(room_id, graph, visited_nodes)

# Create a Graphviz graph
graph = pgv.AGraph(directed=True, rankdir="LR")

# Set the root node
root_node = "!YOUR_ROOT_SPACE_ID:matrix.org"
graph.add_node(root_node, label="YOUR ROOT LABEL")

# Add the spaces and rooms to the graph
visited_nodes = set()
add_nodes_to_graph(root_node, graph, visited_nodes)

# Draw the graph
graph.layout(prog="dot")
graph.write("dot")
graph.draw("matrix_rooms_and_spaces.png")
