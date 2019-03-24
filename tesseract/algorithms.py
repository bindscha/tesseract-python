import math


class Algorithm:
    def __init__(self):
        self.max = math.inf

    def filter(self, e, G):
        return True

    def process(self, e, G):
        print(' * Found match:', e)


class CliqueFinding(Algorithm):
    def __init__(self):
        super().__init__()
        self.max = math.inf

    def filter(self, e, G):
        edges_added_with_expansion = set(filter(lambda edge: edge[1] in e, G.edges(e[-1])))
        return len(edges_added_with_expansion) == len(e) - 1

    def process(self, e, G):
        print(' * Found %d-clique:' % len(e), e)


class ExampleTree(Algorithm):
    def __init__(self):
        super().__init__()
        self.max = 5

    def filter(self, e, G):
        if len(e) < 5:
            return True
        elif len(e) == 5:
            return len(list(filter(lambda v: G.degree(v) > 2, e))) > 0
        return False

    def process(self, e, G):
        if len(e) == 5 and len(list(filter(lambda v: G.degree(v) > 2, e))) > 0:
            print(' * Found tree:', e)
