import unittest

GRAY, BLACK = 0, 1

def topological_sort_recursive(graph):
    order, enter, state = [], set(graph), {}
    
    def dfs(node):
        state[node] = GRAY
        #print(node)
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == GRAY:
                raise ValueError("cycle")
            if sk == BLACK:
                continue
            enter.discard(k)
            dfs(k)
        order.append(node)
        state[node] = BLACK
        
    while enter: dfs(enter.pop())
    return order

def topological_sort(graph):
    order, enter, state = [], set(graph), {}
    
    def is_ready(node):
        lst = graph.get(node, ())
        if len(lst) == 0:
            return True
        for k in lst:
            sk = state.get(k, None)
            if sk == GRAY: raise ValueError("cycle")
            if sk != BLACK:
                return False
        return True
        
    while enter:
        node = enter.pop()
        stack = []
        while True:
            state[node] = GRAY
            stack.append(node)
            for k in graph.get(node, ()):
                sk = state.get(k, None)
                if sk == GRAY: raise ValueError("cycle")
                if sk == BLACK: continue
                enter.discard(k)
                stack.append(k)
            while stack and is_ready(stack[-1]):
                node = stack.pop()
                order.append(node)
                state[node] = BLACK
            if len(stack) == 0:
                break
            node = stack.pop()
        
    return order

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.depGraph = {
                        "a" : [ "b" ],
                        "b" : [ "c" ],
                        "c" :  [ 'e'],
                        'e' : [ 'g' ],
                        "d" : [ ],
                        "f" : ["e" , "d"],
                        "g" : [ ]
                    }
        
    def test_order(self):
        res = topological_sort_recursive(self.depGraph)
        #print(res)
        self.assertTrue(res.index('g') < res.index('e'))
        res = topological_sort_recursive(self.depGraph)
        self.assertTrue(res.index('g') < res.index('e'))

if __name__ == '__main__':
    unittest.main()
