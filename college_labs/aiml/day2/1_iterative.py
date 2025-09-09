import matplotlib.pyplot as plt
import networkx as nx

# ==== User Inputs ====
jug1 = int(input("Enter capacity of Jug 1: "))
jug2 = int(input("Enter capacity of Jug 2: "))
goal = int(input("Enter goal amount in Jug 1: "))

start = (0, 0)
goal_state = (goal, 0)

# ==== Next states ====
def get_next_states(state):
    a, b = state
    moves = set()
    moves.add((jug1, b))
    moves.add((a, jug2))
    moves.add((0, b))
    moves.add((a, 0))
    p = min(a, jug2 - b)  # jug1 -> jug2
    moves.add((a - p, b + p))
    p = min(b, jug1 - a)  # jug2 -> jug1
    moves.add((a + p, b - p))
    return moves

# ==== Heuristic Function ====
def heuristic(node):
    return abs(goal - node[0])

# ==== DLS ====
def dls(node, limit, path, G):
    G.add_node(node)
    if node == goal_state:
        return path
    if len(path) - 1 >= limit:
        return None
    for nxt in get_next_states(node):
        if nxt not in path:
            G.add_edge(node, nxt)
            res = dls(nxt, limit, path + [nxt], G)
            if res:
                return res
    return None

# ==== IDDFS ====
results = []
for depth in range(21):
    G = nx.DiGraph()
    path = dls(start, depth, [start], G)
    results.append((depth, G, path))
    if path:
        break

# ==== Layout for tree ====
def hierarchy_pos(G, root):
    pos = {}
    def dfs(node, x, y, dx):
        pos[node] = (x, y)
        children = list(G.successors(node))
        for i, child in enumerate(children):
            dfs(child, x + (i - (len(children)-1)/2) * dx, y - 1, dx/2)
    dfs(root, 0, 0, 2)
    return pos

# ==== Draw all diagrams on one page ====
def draw_all_in_one(results):
    total = len(results)
    cols = 4
    rows = (total + cols - 1) // cols  # enough rows for all diagrams

    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
    axes = axes.flatten()

    for idx, (depth, G, path) in enumerate(results):
        T = nx.bfs_tree(G, start)
        pos = hierarchy_pos(T, start)

        node_colors = [
            "lightgreen" if n == goal_state else
            "lightcoral" if path and n in path else
            "skyblue"
            for n in T.nodes()
        ]
        edge_colors = [
            "red" if path and e[0] in path and e[1] in path and
            path.index(e[1]) == path.index(e[0]) + 1 else "black"
            for e in T.edges()
        ]

        labels = {n: f"{n}\n[h={heuristic(n)}]" for n in T.nodes()}

        nx.draw(
            T, pos,
            with_labels=True,
            labels=labels,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=900,
            font_size=7,
            arrows=True,
            arrowsize=8,
            width=1,
            ax=axes[idx]
        )

        if path:
            axes[idx].set_title(f"Depth {depth} (Goal Found)", fontsize=11)
        else:
            axes[idx].set_title(f"Depth {depth}", fontsize=11)

    # Hide any unused subplots
    for ax in axes[len(results):]:
        ax.axis("off")

    plt.tight_layout()
    plt.suptitle(f"IDDFS Search Progress – All Depths", fontsize=14, y=1.02)
    plt.show()

draw_all_in_one(results)

# ==== Print goal info ====
for depth, G, path in results:
    if path:
        print(f"\nGoal found at depth {depth}")
        print("Path:", " -> ".join(map(str, path)))
        print("Distances from root:")
        for i, node in enumerate(path):
            print(f"  {node}: depth={i}, h={heuristic(node)}")
        break