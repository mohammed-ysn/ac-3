def colour_graph(graph, actions):
    colours = {"r", "c", "b"}
    domain = {node: colours.copy() for node in graph}

    for node, colour in actions:
        print(f"Setting {node}={colour}")
        domain[node] = {colour}
        if not forward_check(node, colour, graph, domain):
            print("Forward check failed")
            break
        if not ac3(graph, domain):
            print("AC-3 failed")
            break
        print(f"Resultant domain: {domain}\n")
    return domain


def forward_check(updated_node, colour, graph, domain):
    for neighbour in graph[updated_node]:
        domain[neighbour].discard(colour)
        if len(domain[neighbour]) == 0:
            return False
    return True


def ac3(graph, domain):
    queue = {(x, y) for x in graph for y in graph[x]}

    while queue:
        (xi, xj) = queue.pop()

        if revise(domain, xi, xj):
            if len(domain[xi]) == 0:
                return False

            for xk in graph[xi]:
                if xk != xj:
                    queue.add((xk, xi))

    return True


def revise(domain, xi, xj):
    to_remove = set()
    for colour in domain[xi]:
        if not any(colour != k for k in domain[xj]):
            to_remove.add(colour)
    domain[xi].difference_update(to_remove)
    return len(to_remove) > 0


graph = {
    1: [2, 3, 4],
    2: [1, 4, 6],
    3: [1, 4, 7],
    4: [1, 2, 3, 5],
    5: [4, 6, 7],
    6: [2, 5, 7, 8],
    7: [3, 5, 6, 8],
    8: [6, 7],
}

actions = [(1, "r"), (4, "c"), (5, "r"), (8, "c"), (6, "b")]

final_domain = colour_graph(graph, actions)
print(f"Final domain: {final_domain}")
