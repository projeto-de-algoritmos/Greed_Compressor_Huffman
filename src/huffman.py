class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        self.arvore = None

    def __lt__(self, other):
        return self.freq < other.freq

    def count_nodes(self):
        if self.char is not None:
            return 1
        left_count = self.left.count_nodes() if self.left else 0
        right_count = self.right.count_nodes() if self.right else 0
        return 1 + left_count + right_count
