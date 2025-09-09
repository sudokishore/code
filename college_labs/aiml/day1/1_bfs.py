import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

JUG1_CAPACITY = 4
JUG2_CAPACITY = 3
GOAL_STATE = (2, 0)

def get_successors(state):
    successors = set()
    a, b = state
    successors.add((JUG1_CAPACITY, b))
    successors.add((a, JUG2_CAPACITY))
    successors.add((0, b))
    successors.add((a, 0))

    pour = min(a, JUG2_CAPACITY - b)
    successors.add((a - pour, b + pour))

    pour = min(b, JUG1_CAPACITY - a)
    successors.add((a + pour, b - pour))

    return successors

def bfs_with_animation(start):
    G = nx.DiGraph()
    visited = set()
    parent = {}
    queue = deque([start])
    visited.add(start)
    parent[start] = None
    G.add_node(start)

    pos = {}
    fig, ax = plt.subplots(figsize=(10, 6))

    def draw_tree(current_node, path_nodes=None):
        ax.clear()
        ax.set_title(f"Exploring: {current_node}", fontsize=14)
        pos.clear()

        def assign_pos(node, depth=0, x=0):
            if node not in pos:
                pos[node] = (x, -depth)
                children = list(G.successors(node))
                if children:
                    start_x = x - len(children) / 2
                    for i, child in enumerate(children):
                        assign_pos(child, depth + 1, start_x + i)

        assign_pos(start)
        colors = []
        for node in G.nodes:
            if path_nodes and node in path_nodes:  
                colors.append("lightgreen")
            elif node == current_node:
                colors.append("orange")
            else:
                colors.append("lightblue")

        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, ax=ax)
        plt.pause(0.6)

    goal_found = None

    while queue:
        current = queue.popleft()

        if current == GOAL_STATE:  
            print("Goal reached:", current)
            goal_found = current  
            path_nodes = []
            temp = current
            while temp is not None:
                path_nodes.append(temp)
                temp = parent[temp]
            path_nodes.reverse()
            draw_tree(current, path_nodes)
            break

        for succ in get_successors(current):
            if succ not in visited:
                visited.add(succ)
                parent[succ] = current
                G.add_edge(current, succ)
                draw_tree(succ)
                queue.append(succ)

    if goal_found:  
        path = []
        temp = goal_found
        while temp is not None:
            path.append(temp)
            temp = parent[temp]
        path.reverse()
        edge_path = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color='red', width=2, ax=ax)
        plt.pause(1)

    plt.show()

start_state = (0, 0)
bfs_with_animation(start_state)
