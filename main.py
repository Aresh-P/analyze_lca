from collections import defaultdict
import copy
import matplotlib.pyplot as plt

class Node:
    def __init__(self, parent):
        self.parent = parent
    def get_parent(self):
        global N_ADVANCES
        N_ADVANCES += 1
        return self.parent

class NodeRef:
    def __init__(self, origin, n_parents, node):
        self.origin = origin
        self.n_parents = n_parents
        self.node = node
    def get_parent(self):
        return NodeRef(self.origin, self.n_parents+1, self.node.get_parent())
    def __eq__(self, other):
        global PAIRS
        if self.origin < other.origin:
            PAIRS[(self.origin, other.origin)].append((self.n_parents, other.n_parents))
        else:
            PAIRS[(other.origin, self.origin)].append((other.n_parents, self.n_parents))
        return self.node == other.node

def find_depth_difference(a, b):
    if a == b:
        return 0
    g = 1
    while True:
        d = test_depth_diff(g, copy.copy(a), copy.copy(b))
        if d is not None:
            return d
        d = test_depth_diff(g, copy.copy(b), copy.copy(a))
        if d is not None:
            return -d
        g *= 2

def test_depth_diff(g, a, b):
    for _ in range(g):
        a = a.get_parent()
    if a == b:
        return g
    for d in range(g):
        b = b.get_parent()
        if b == a:
            return g - (d + 1)
    return None
        
def get_ptrs(lca_to_root, a_to_lca, b_to_lca):
    root = Node(None)
    lca = root
    for _ in range(lca_to_root):
        lca = Node(lca)
    a = lca
    for _ in range(a_to_lca):
        a = Node(a)
    b = lca
    for _ in range(b_to_lca):
        b = Node(b)
    return NodeRef("a", 0, a), NodeRef("b", 0, b)



def main():
    global N_ADVANCES
    global PAIRS
    root_to_lca = 10000
    params = list((0, 2**i+1) for i in range(7))
    for lca_to_a, lca_to_b in params:
        N_ADVANCES = 0
        PAIRS = defaultdict(list)
        print(f"Distances from LCA: {lca_to_a}, {lca_to_b}")
        a, b = get_ptrs(root_to_lca, lca_to_a, lca_to_b)
        d = find_depth_difference(a, b)
        print(f"Computed distance: {d}")
        print(f"# advances: {N_ADVANCES}")
        print(f"Predicted worst case (15k-20): {15*(lca_to_a+lca_to_b)-20}")
        ax = plt.gca()
        ax.set_aspect('equal')
        plt.plot(*zip(*PAIRS[("a", "b")]), '.')
        plt.show()

if __name__ == "__main__":
    main()
