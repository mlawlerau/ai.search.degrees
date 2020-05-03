class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []
        # maintain an additional hash set of states for O(1) lookup in contains_state()
        self.states = set()

    def add(self, node):
        self.frontier.append(node)
        self.states.add(node.state)

    def contains_state(self, state):
        # This original line is O(N) slow, faster to use O(1) hashset lookup
        # return any(node.state == state for node in self.frontier)
        return state in self.states

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            self.states.remove(node.state)
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            self.states.remove(node.state)
            return node
