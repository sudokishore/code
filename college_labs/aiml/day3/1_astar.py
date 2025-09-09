import matplotlib.pyplot as plt
import networkx as nx
import math
import numpy as np

# ------------------- User Input -------------------
try:
    jug1, jug2 = map(int, input("Jug1 Jug2 capacity: ").split())
    goal = tuple(map(int, input("Goal jug1 jug2: ").split()))
except Exception:
    print("Invalid input or running non-interactively — using defaults: jug1=4, jug2=3, goal=(2,0)")
    jug1, jug2 = 4, 3
    goal = (2, 0)

# ------------------- Custom Heuristic -------------------
def heuristic(state):
    x, y = state
    if 0 < x < jug1 and 0 < y < jug2:
        return 2
    elif (0 < x < jug1 and y == 0) or (x == 0 and 0 < y < jug2):
        return 4
    elif (x == 0 and y == 0) or (x == jug1 and y == jug2):
        return 10
    elif (x == 0 and y == jug2) or (x == jug1 and y == 0):
        return 8
    else:
        return 0

# ------------------- Successor function -------------------
def successors(state):
    a, b = state
    succ = {
        (jug1, b),  # Fill jug1
        (a, jug2),  # Fill jug2
        (0, b),     # Empty jug1
        (a, 0),     # Empty jug2
        (a - min(a, jug2 - b), b + min(a, jug2 - b)),  # Pour jug1 -> jug2
        (a + min(b, jug1 - a), b - min(b, jug1 - a))   # Pour jug2 -> jug1
    }
    succ.discard(state)
    return succ

# ------------------- A* style search -------------------
start = (0, 0)
stack = [start]
visited = {start}
visit_order = [start]
parent = {start: None}
g_cost = {start: 0}  # g(n)

snapshots = [(set(visited), start, set())]
found = False

while stack:
    stack.sort(key=heuristic, reverse=True)
    current = stack.pop()

    if current == goal:
        snapshots.append((set(visited), current, set()))
        found = True
        break

    next_states = successors(current)
    new_nodes = set()

    for nxt in sorted(next_states, key=heuristic):
        if nxt not in visited:
            visited.add(nxt)
            visit_order.append(nxt)
            parent[nxt] = current
            g_cost[nxt] = g_cost[current] + 1
            stack.append(nxt)
            new_nodes.add(nxt)

    snapshots.append((set(visited), current, new_nodes))

if not found and visit_order:
    last = visit_order[-1]
    snapshots.append((set(visited), last, set()))

# ------------------- Build directed tree -------------------
G = nx.DiGraph()
for child, par in parent.items():
    if par is not None:
        G.add_edge(par, child)
for n in visited:
    if n not in G:
        G.add_node(n)

# ------------------- Compute fixed positions (wider spacing) -------------------
def compute_positions(G, root, width=1.8, vert_gap=0.25, vert_loc=0, horiz_center=0.5, pos=None, parent_node=None):
    if pos is None:
        pos = {}
    pos[root] = (horiz_center, vert_loc)
    children = list(G.successors(root))
    if parent_node in children:
        children.remove(parent_node)
    children = sorted(children)
    if children:
        dx = width / len(children)
        left = horiz_center - width / 2 - dx / 2
        for child in children:
            left += dx
            compute_positions(G, child, dx, vert_gap, vert_loc - vert_gap, left, pos, root)
    return pos

if start in G.nodes() and len(G.nodes()) > 1:
    pos = compute_positions(G, start)
else:
    pos = nx.spring_layout(G, seed=42)
    if start not in pos:
        pos[start] = (0.5, 0.0)

# ------------------- Reconstruct full solution path -------------------
solution_path = []
if found:
    node = goal
    while node is not None:
        solution_path.append(node)
        node = parent[node]
    solution_path.reverse()

# ------------------- Helper: make node labels -------------------
def make_labels(nodes, g_cost, heuristic):
    labels = {}
    for n in nodes:
        g = g_cost.get(n, math.inf)
        h = heuristic(n)
        f = g + h
        labels[n] = f"{n}\ng={g},h={h},f={f}"
    return labels

# ------------------- Plot snapshots -------------------
num = len(snapshots)
cols = min(4, num if num else 1)
rows = math.ceil((num if num else 1) / cols)
fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))

if isinstance(axes, np.ndarray):
    axes_flat = axes.flatten().tolist()
else:
    axes_flat = [axes]

for idx, (visited_i, current, new_nodes) in enumerate(snapshots):
    ax = axes_flat[idx]
    if idx == 0:
        ax.set_title(f"Step {idx}: Start {current}", fontsize=10)
    else:
        newly = ", ".join(map(str, sorted(new_nodes))) if new_nodes else "(no new nodes)"
        ax.set_title(f"Step {idx}: expand {current} → {newly}", fontsize=9)

    visited_list = sorted(visited_i)
    node_colors = []
    for n in visited_list:
        if idx == len(snapshots) - 1 and found and n in solution_path:
            node_colors.append("yellow")
        elif n == goal:
            node_colors.append("violet")
        elif n in new_nodes:
            node_colors.append("lightgreen")
        elif n == current:
            node_colors.append("orange")
        else:
            node_colors.append("lightblue")

    nx.draw_networkx_nodes(G, pos, nodelist=visited_list,
                           node_color=node_colors, node_size=950, ax=ax)

    # Labels inside nodes
    labels = make_labels(visited_list, g_cost, heuristic)
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=7)

    # Edges
    edges_to_draw = [(parent[child], child) for child in visited_list if parent.get(child) in visited_i]
    edge_colors, edge_widths = [], []
    for u, v in edges_to_draw:
        if found and u in solution_path and v in solution_path:
            edge_colors.append("red")
            edge_widths.append(2.5)
        elif v == current:
            edge_colors.append("orange")
            edge_widths.append(2.0)
        else:
            edge_colors.append("gray")
            edge_widths.append(1.2)

    nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, ax=ax,
                           edge_color=edge_colors, width=edge_widths,
                           arrows=True, arrowsize=12)

    ax.set_axis_off()

for j in range(len(snapshots), rows * cols):
    axes_flat[j].axis('off')

plt.suptitle("Step-by-step Expansion with g,h,f values", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])

outname = 'water_jug_steps_clear.png'
plt.savefig(outname, dpi=200)
print(f"\nSaved step-by-step figure to {outname}")
plt.show()

# ------------------- Print values in console -------------------
print("\nNode   g   h   f")
for n in visit_order:
    g = g_cost.get(n, math.inf)
    h = heuristic(n)
    f = g + h
    print(f"{n}   g={g}, h={h}, f={f}")
