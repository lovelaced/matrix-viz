# Matrix Spaces and Rooms Graph (visualizer)

This script creates a directed acyclic graph (DAG) of the rooms and spaces within a Matrix instance. It does this by starting at a specified root space and recursively searching for all of its child spaces and rooms. The graph is created using the PyGraphviz library and is rendered as a .png file.

To use this script, you will need to obtain an access token for a user on the Matrix instance. You will also need to specify the root space ID and label for the graph.

To install the required libraries, run:

`pip install pygraphviz matrix-client`

To use the script, fill in the `ACCESS_TOKEN`, `root_node`, and root label variables in the script and run:

`python matrix_viz.py`

The resulting .png file will be saved in the same directory as the script.
