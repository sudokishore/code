import networkx as nx
import matplotlib.pyplot as plt
import time

def can_split(pile):
    return pile > 2

def generate_moves(pile):
    moves = []
    for i in range(1, pile // 2 + 1):
        j = pile - i
        if i != j:
            moves.append((i, j))
    return moves

def evaluate(state, is_max_turn, G, parent=None, depth=0):
    state = sorted(state) 
    state_str = "+".join(map(str, state))
    label = f"{state_str}\n({'MAX' if is_max_turn else 'MIN'})"

    G.add_node(label, depth=depth)
    if parent:
        G.add_edge(parent, label)

    if not any(can_split(pile) for pile in state):
        value = -1 if is_max_turn else +1
        G.nodes[label]['value'] = value
        return value

    if is_max_turn: 
        best = float('-inf')
        for i, pile in enumerate(state):
            if not can_split(pile):
                continue
            for move in generate_moves(pile):
                new_state = state[:i] + list(move) + state[i+1:]
                val = evaluate(new_state, False, G, label, depth+1)
                best = max(best, val)
        G.nodes[label]['value'] = best
        return best
    else:  
        best = float('inf')
        for i, pile in enumerate(state):
            if not can_split(pile):
                continue
            for move in generate_moves(pile):
                new_state = state[:i] + list(move) + state[i+1:]
                val = evaluate(new_state, True, G, label, depth+1)
                best = min(best, val)
        G.nodes[label]['value'] = best
        return best

def animate_tree(G):
    depths = nx.get_node_attributes(G, "depth")
    layers = {}
    for n, d in depths.items():
        layers.setdefault(d, []).append(n)
    pos = {}
    for d in sorted(layers.keys()):
        nodes = layers[d]
        if not nodes:
            continue
        count = len(nodes)
        xs = [i - (count-1)/2 for i in range(count)] 
        for x, n in zip(xs, nodes):
            pos[n] = (x, -d)

    max_depth = max(depths.values()) if depths else 0
    plt.figure(figsize=(22, 10))

    for d in range(max_depth + 1):
        nodes_at_depth = [n for n in G.nodes if depths.get(n, 0) == d]
        edges_at_depth = [(u, v) for u, v in G.edges if depths.get(v, 0) == d]

        nx.draw_networkx_nodes(G, pos, nodelist=nodes_at_depth,
            node_size=2000, node_color="orange")
        nx.draw_networkx_labels(
            G, pos,
            labels={n: f"{n}\nVal={G.nodes[n].get('value','')}" for n in nodes_at_depth},
            font_size=8, font_weight="bold"
        )
        nx.draw_networkx_edges(G, pos, edgelist=edges_at_depth, arrows=True)
        plt.pause(1)

    plt.axis("off")
    plt.tight_layout()
    plt.show()
G = nx.DiGraph()
n=int(input("Enter the number :"))
initial_pile = [n]
result = evaluate(initial_pile, False, G)
print("Game Result:", "Max Wins" if result == 1 else "Min Wins")
animate_tree(G)