from collections import defaultdict
import copy
import matplotlib.pyplot as plt
from abc import ABC

class Logger:
    def __init__(self):
        self.n_advances = 0
        self.pairs = defaultdict(list)
    
LOGGER = Logger()

class Node:
    def __init__(self, parent):
        self.parent = parent
    def get_parent(self):
        global LOGGER
        LOGGER.n_advances += 1
        return self.parent

class NodeRef:
    def __init__(self, origin, n_parents, node):
        self.origin = origin
        self.n_parents = n_parents
        self.node = node
    def get_parent(self):
        return NodeRef(self.origin, self.n_parents+1, self.node.get_parent())
    def __eq__(self, other):
        global LOGGER
        if self.origin < other.origin:
            LOGGER.pairs[(self.origin, other.origin)].append((self.n_parents, other.n_parents))
        else:
            LOGGER.pairs[(other.origin, self.origin)].append((other.n_parents, self.n_parents))
        return self.node == other.node

class LCAAlgo(ABC):

    def __init__(self, logger):
        pass

    def reset_logger(self):
        pass

    def find_lca(self, a, b):
        pass

class LCAAlgo1(LCAAlgo):

    def __init__(self, logger):
        self.logger = logger

    def reset_logger(self):
        self.logger = Logger()
        
    def test_depth_diff(self, g, a, b):
        for _ in range(g):
            a = a.get_parent()
        if a == b:
            return g
        for d in range(g):
            b = b.get_parent()
            if b == a:
                return g - (d + 1) # Fixed off-by-one because b is advanced first
        return None
    
    def find_depth_difference(self, a, b):
        if a == b:
            return 0
        g = 1
        while True:
            d = self.test_depth_diff(g, copy.copy(a), copy.copy(b))
            if d is not None:
                return d
            d = self.test_depth_diff(g, copy.copy(b), copy.copy(a))
            if d is not None:
                return -d
            g *= 2

    def find_lca(self, a, b):

        # Passing logger to all functions is annoying, but may want multiple loggers
        # Compromise: swap out global variable for duration of algorithm
        global LOGGER
        og_logger = LOGGER
        LOGGER = self.logger
        
        d = self.find_depth_difference(a, b)
        if d > 0:
            for _ in range(d):
                a = a.get_parent()
        if d < 0:
            for _ in range(-d):
                b = b.get_parent()
        while a != b:
            a = a.get_parent()
            b = b.get_parent()

        self.logger = LOGGER
        LOGGER = og_logger
        
        return a
        
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
    root_to_lca = 10000
    params = list((0, 2**i+1) for i in range(7))
    for lca_to_a, lca_to_b in params:
        
        logger = Logger()
        algo1 = LCAAlgo1(logger)
        
        print(f"Distances from LCA: {lca_to_a}, {lca_to_b}")
        a, b = get_ptrs(root_to_lca, lca_to_a, lca_to_b)
        lca = algo1.find_lca(a, b)
        print(f"# advances: {algo1.logger.n_advances}")
        print(f"Predicted worst case (16k-20): {16*(lca_to_a+lca_to_b)-20}")
        ax = plt.gca()
        ax.set_aspect('equal')
        plt.plot(*zip(*algo1.logger.pairs[("a", "b")]), '.')
        plt.plot(lca_to_a, lca_to_b, 'o', color='orange')
        plt.show()

if __name__ == "__main__":
    main()
